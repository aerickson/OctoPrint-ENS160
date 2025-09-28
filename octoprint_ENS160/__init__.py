# coding=utf-8
from __future__ import absolute_import

import adafruit_ens160
import board

import octoprint.plugin
import octoprint.util

from .libs.config import parse_sensor_config, ENS160ParseException


class ENS160Plugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
):
    def __init__(self):
        self.sensors = {}  # strings
        self.sensor_objects = {}
        self.current_data = {}  # {sensor_name: {'tvoc': 123, 'eco2': 456, 'aqi': 3}}
        self.timer = None

    def on_after_startup(self):
        # self._logger.info("startup")
        try:
            self.sensors = parse_sensor_config(
                self._settings.get(["pin_configuration"])
            )
        except ENS160ParseException as e:
            self._logger.error(
                "on_after_startup: parse error when reading settings, exception: %s" % e
            )
            self._logger.error(e)

        i2c = board.I2C()
        for name, pin in self.sensors.items():
            self.sensor_objects[name] = adafruit_ens160.ENS160(
                i2c, int(pin, 16)
            )
            # TODO: expose these as settings
            self.sensor_objects[name].temperature_compensation = 25
            self.sensor_objects[name].humidity_compensation = 50

        self._logger.info(
            "startup: pin_configuration: %s" % self._settings.get(["pin_configuration"])
        )
        self.start_timer()
        # self._logger.info("exit on_after_startup")

    # ~~ TemplatePlugin
    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    ##~~ SettingsPlugin mixin
    def on_settings_save(self, data):
        self._logger.info("in on_settings_save")
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

    def get_settings_defaults(self):
        self._logger.info("in get_settings_defaults")
        return dict(
            debugging_enabled=False, pin_configuration="Enclosure:41,External:40"
        )

    def get_settings_restricted_paths(self):
        return dict(
            admin=[["debugging_enabled"], ["pin_configuration"],], user=[], never=[]
        )

    def get_settings_version(self):
        return 1

    # see https://docs.octoprint.org/en/maintenance/plugins/hooks.html?highlight=octoprint%20comm%20protocol#octoprint-comm-protocol-temperatures-received
    def callback(self, comm, parsed_temps):
        # parsed_temps.update(test = (random.uniform(99,101),100))
        # parsed_temps.update(test2 = (random.uniform(199,201),200))
        # parsed_temps.update(test3 = (random.uniform(55,57),None))
        # return parsed_temps

        # parsed_temps["clown123"] = (random.uniform(22,24),None)

        # self._logger.info("in callback")
        for sensor_name, readings_dict in self.current_data.items():
            parsed_temps[f"ens160_{sensor_name}_tvoc"] = (readings_dict.get("tvoc"), None)
            parsed_temps[f"ens160_{sensor_name}_eco2"] = (readings_dict.get("eco2"), None)
            parsed_temps[f"ens160_{sensor_name}_aqi"] = (readings_dict.get("aqi"), None)
        return parsed_temps

    def do_work(self):
        # self._logger.info("in doWork")
        for name, sensor_obj in self.sensor_objects.items():
            try:
                aqi = sensor_obj.AQI
                tvoc = sensor_obj.TVOC
                eco2 = sensor_obj.eCO2
                self.current_data[name] = {"aqi": aqi, "tvoc": tvoc, "eco2": eco2}
                self._logger.debug("%s: %s" % (name, self.current_data[name]))
            except Exception as error:
                self._logger.debug("exception: %s" % error.args[0])

    def start_timer(self):
        # TODO: allow this to be configured?
        # interval = self._settings.get_float(["interval"])
        interval = 2
        # self._logger.info(
        #     "starting timer to run command '%s' every %s seconds" % (the_cmd, interval)
        # )
        self.timer = octoprint.util.RepeatedTimer(
            interval, self.do_work, run_first=True
        )
        self.timer.start()

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            ENS160=dict(
                displayName="ENS160 Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_commit",
                user="aerickson",
                repo="OctoPrint-ENS160",
                branch="master",
                pip="https://github.com/aerickson/OctoPrint-ENS160/archive/{target}.zip",
                current=self._plugin_version,
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "ENS160 Plugin"
__plugin_pythoncompat__ = ">=3.7,<4"  # python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ENS160Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        # https://docs.octoprint.org/en/maintenance/plugins/hooks.html?highlight=octoprint%20comm%20protocol#execution-order
        "octoprint.comm.protocol.temperatures.received": (
            __plugin_implementation__.callback,
            1,
        ),  # function and order
    }
