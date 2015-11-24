import sublime
import sublime_plugin
import json
import os.path
import sys
from sublime_plugin import EventListener

TOGGLE_TABS = 'toggle_tabs'


class Listener(EventListener):

    def on_window_command(self, window, command, option):
        # toggle_tabs command except it does not control.
        if(command != TOGGLE_TABS):
            return

        if(option == 'hide_tabs' and TabStatusContainer.getTabCloseFlag() == True):
            # set tab hide flag.
            TabStatusContainer.setShowTabStatus(False)
        elif(TabStatusContainer.getTabCloseFlag() == False):
            # set tab show/hide flag.
            TabStatusContainer.setShowTabStatus(
                not TabStatusContainer.getShowTabStatus())
        else:
            # force disable disable the tab control of the menu.
            return ('None')


class TabStatusContainer():
    # show_tabs parameter from Session.sublime_session.
    _show_tab_status = {}

    # auto tab closing flag.
    _tab_close_flag = None

    @staticmethod
    def getActiveWindowId():
        return sublime.active_window().id()

    @classmethod
    def getShowTabStatus(store):
        # get active window_id
        window_id = store.getActiveWindowId()

        if(not window_id in store._show_tab_status):
            store._show_tab_status[window_id] = None

        return store._show_tab_status[window_id]

    @classmethod
    def setShowTabStatus(store, status):
        # get active window_id
        window_id = store.getActiveWindowId()

        # set show_tab_status.
        store._show_tab_status[window_id] = status

    @classmethod
    def getTabCloseFlag(store):
        return store._tab_close_flag

    @classmethod
    def setTabCloseFlag(store, flag):
        store._tab_close_flag = flag


class SidebarSeparator(sublime_plugin.TextCommand):

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

        # set auto tab closing flag.
        TabStatusContainer.setTabCloseFlag(setting_values['auto_tab_hide'])

        # check auto hide option.
        if(TabStatusContainer.getTabCloseFlag() != True):
            return

        # to determine the need for command execution
        if(self.checkShowTabStatus() != True):
            return

        # execute hide tabs.
        self.hideTabBar(setting_values)

    def getSettingValues(self):

        # config files(user)
        config_file = 'sidebar_separator.sublime-settings'

        # get config value from setting file.
        setting_values = {}
        try:
            settings = sublime.load_settings(config_file)

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

    def checkShowTabStatus(self):
        # check show_tabs parameter at global.
        if (TabStatusContainer.getShowTabStatus() is None):

            # set show_tabs parameter from Session.sublime_session.
            TabStatusContainer.setShowTabStatus(self.getJsonParameter())

        if(TabStatusContainer.getShowTabStatus() == True):
            return True
        else:
            return False

    def hideTabBar(self, setting_values):
        # hide tabbar.
        sublime.active_window().run_command(TOGGLE_TABS, 'hide_tabs')

    def checkSettingFileExists(self):
        # set path of setting file.
        path = sublime.packages_path().replace('Packages', '')
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
