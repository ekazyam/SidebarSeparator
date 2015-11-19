import sublime
import sublime_plugin
import json
import os.path
import sys
import re


class SidebarSeparator(sublime_plugin.TextCommand):

    # show_tabs parameter from Session.sublime_session.
    show_tab_status = None

    @staticmethod
    def getShowTabStatus():
        return SidebarSeparator.show_tab_status

    @staticmethod
    def setShowTabStatus(status):
        SidebarSeparator.show_tab_status = status

    def run(self, edit):
        # get setting values from setting file.
        setting_values = self.getSettingValues()

        # set separate data.
        separate_value = self.setSeparate(setting_values)

        # create separate file.
        separate_file = sublime.active_window().new_file()

        # set buffer name.
        separate_file.set_name(separate_value)

        # set not save as separate file propertie.
        separate_file.set_scratch(True)

        # set read only propertie.
        separate_file.set_read_only(True)

        # hide tabbar.
        self.hideTabBar(setting_values)

    def getSettingValues(self):
        # get separate value from setting file.
        setting_values = {}
        try:
            settings = sublime.load_settings(
                'SidebarSeparator.sublime-settings')
            setting_values["separate_value"] = settings.get(
                'separate_value', '-')
            setting_values["separate_count"] = settings.get(
                'separate_count', 100)
            setting_values["auto_tab_hide"] = settings.get(
                'auto_tab_hide', True)
        except:
            pass
        return setting_values

    def setSeparate(self, setting_values):
        # set separate value
        return setting_values["separate_value"] * setting_values["separate_count"]

    def getJsonParameter(self):
        # check setting file exist.
        # Auto Save File or Other.
        setting_file = self.checkSettingFileExists()

        # get json file from setting file.
        setting_data = self.loadSettingData(setting_file)

        return setting_data['windows'][0]['show_tabs']

    def hideTabBar(self, setting_values):
        # check auto_hide_tab parameter.
        if(setting_values['auto_tab_hide'] != True):
            return

        # to make sure that it is not set in global parameter.
        if (SidebarSeparator.getShowTabStatus() is None):

            # set show_tabs parameter from Session.sublime_session.
            SidebarSeparator.setShowTabStatus(self.getJsonParameter())

        # check show_tabs parameter at global.
        if (SidebarSeparator.getShowTabStatus() == True):

            # set show_tab_status at static values.
            SidebarSeparator.setShowTabStatus(False)

            # hide tabbar.
            sublime.active_window().run_command('toggle_tabs')

    def checkSettingFileExists(self):
        # set path of setting file.
        path = re.sub(r'Packages$', '', sublime.packages_path())
        if(sublime.platform() == 'windows'):
            # for windows.
            setting_files = (path + '\Local\Auto Save Session.sublime_session',
                             path + '\Local\Session.sublime_session')
        else:
            # for mac/linux.
            setting_files = (path + '/Local/Auto Save Session.sublime_session',
                             path + '/Local/Session.sublime_session')

        # check setting file exist.
        if(os.path.isfile(setting_files[0])):
            return setting_files[0]
        elif(os.path.isfile(setting_files[1])):
            return setting_files[1]
        sys.exit

    def loadSettingData(self, setting_file):
        # load json from setting file.
        return json.loads(
            open(setting_file, 'r', encoding="utf8").read(), strict=False)
