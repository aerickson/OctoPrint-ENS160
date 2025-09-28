/*
 * View model for OctoPrint-ENS160
 *
 * Author: Andrew J. Erickson
 * License: AGPLv3
 */
$(function() {
    function ENS160ViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: ENS160ViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ ],
        // dependencies: [ "loginStateViewModel", "settingsViewModel" ],

        // Elements to bind to, e.g. #settings_plugin_ENS160, #tab_plugin_ENS160, ...
        elements: []
        // elements: [ "#settings_plugin_ENS160" ]
    });
});
