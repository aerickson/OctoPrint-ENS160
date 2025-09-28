# ake pin_config

class ENS160Exception(Exception):
    pass


class ENS160ParseException(ENS160Exception):
    pass


def parse_sensor_config(pin_config_string):
    sensors = {}
    try:
        conf_pairs = pin_config_string.split(',')
        for item in conf_pairs:
            pair = item.split(':')
            name = pair[0]
            pin = pair[1]
            sensors[name] = pin
            # print("%s: %s" %name, pin)
    except Exception as e:
        raise ENS160ParseException("parse_sensor_config: parse error, exception: %s" % e)
    return sensors


if __name__ == "__main__":
    # execute only if run as a script
    import pprint
    pprint.pprint(parse_sensor_config('Abc:31,DDD:22'))
