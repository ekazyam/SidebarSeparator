import sublime
import json
import os.path
from sublime_plugin import TextCommand
from sublime_plugin import EventListener


def plugin_loaded():
    # update settings.
    SettingStore().update_settings()

    # update config.
    SettingStore().update_config()

    # add settings modified listener.
    SettingStore().settings.add_on_change(
        'reload', SettingStore().update_settings)


class TabControlListener(EventListener):

    def on_window_command(self, window, command, option):
        def _new_window():
            TabStatusStore().active_window_status = TabStatusStore().get_show_tab_status()

        def _toggle_tabs(command, option):
            if(option == 'sidebar_separator' and SettingStore().get_auto_hide_option(
            ) and TabStatusStore().get_show_tab_status()):
                # set tab hide flag.
                TabStatusStore().set_show_tab_status(False)
                return True
            elif(not SettingStore().get_auto_hide_option()):
                TabStatusStore().toggle_show_tab_status()
                return True
            elif(SettingStore().get_auto_hide_option()):
                return False
            return False

        if(command == 'toggle_tabs'):
            if (not _toggle_tabs(command, option)):
                return ('None')
        elif(command == 'new_window'):
            _new_window()


class TabStatusStore():
    # singleton instance.
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(TabStatusStore, cls).__new__(
                cls, *args, **kwargs)

            # show_tabs parameter from Session.sublime_session.
            cls.__show_tab_status = {}

            # just before active window status.
            cls.__active_window_status = None

        return cls.__instance

    @property
    def active_window_status(self):
        return self.__active_window_status

    @active_window_status.setter
    def active_window_status(self, status):
        self.__active_window_status = status

    def get_show_tab_status(self):
        # get active window_id
        window_id = sublime.active_window().id()

        if(not window_id in self.__show_tab_status):
            # set just before active window id.
            self.__show_tab_status[window_id] = self.__active_window_status

        return self.__show_tab_status[window_id]

    def set_show_tab_status(self, status):
        # get active window_id
        window_id = sublime.active_window().id()

        # set show_tab_status.
        self.__show_tab_status[window_id] = status

    def toggle_show_tab_status(self):
        # get active window_id
        window_id = sublime.active_window().id()

        self.__show_tab_status[
            window_id] = not self.get_show_tab_status()


class SettingStore():
    # singleton instance.
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(SettingStore, cls).__new__(
                cls, *args, **kwargs)

            # initial value of the setting file.
            cls.__settings = None

            # initial value of the configuration file.
            cls.__config = None

        return cls.__instance

    @property
    def config(self):
        return self.__config

    @config.setter
    def set_config(self, config):
        self.__config = config

    @property
    def settings(self):
        return self.__settings

    @settings.setter
    def settings(self, settings):
        self.__settings = settings

    def update_config(self):
        def _load_config():
            def _parse_json(config_file):
                # parse json from config file.
                opened_file = open(config_file, 'r', encoding="utf8")
                return json.loads(opened_file.read(), strict=False)

            path = sublime.packages_path().replace('Packages', '')

            if(sublime.platform() == 'windows'):
                # for windows.
                config_files = (path + '\Local\Auto Save Session.sublime_session',
                                path + '\Local\Session.sublime_session')
            else:
                # for mac/linux.
                config_files = (path + '/Local/Auto Save Session.sublime_session',
                                path + '/Local/Session.sublime_session')

            # preferentially set automatic writing file.
            if(os.path.isfile(config_files[0])):
                config_file = config_files[0]
            else:
                config_file = config_files[1]

            return _parse_json(config_file)

        if(SettingStore().config is None):
            SettingStore().config = _load_config()

        TabStatusStore().set_show_tab_status(
            SettingStore().get_tab_visibility_option())

    def update_settings(self):
        # load settings value from setting file.
        self.settings = sublime.load_settings(
            'sidebar_separator.sublime-settings')

    def get_auto_hide_option(self):
        # get auto_tab_hide option and return the flag.
        auto_hide_flag = self.settings.get('auto_tab_hide', True)

        return auto_hide_flag

    def get_tab_visibility_option(self):
        return self.config['windows'][0]['show_tabs']


class SidebarSeparator(TextCommand):

    def run(self, edit):
        # create separate file.
        self.create_separater()

        # auto tab hide.
        self.hide_tab_bar()

    def create_separater(self):
         # create separate file.
        separate_file = sublime.active_window().new_file()

        # set buffer name.
        separate_file.set_name(self.get_separate_value())

        # set not save as separate file propertie.
        separate_file.set_scratch(True)

        # set read only propertie.
        separate_file.set_read_only(True)

    def hide_tab_bar(self):
        # controlling the tabs when the flag is true.
        if(SettingStore().get_auto_hide_option() and TabStatusStore().get_show_tab_status()):

            active_window = sublime.active_window()
            active_window.run_command('toggle_tabs', 'sidebar_separator')

    def get_separate_value(self):
        # get separate value and create separater.
        value = SettingStore().settings.get('separate_value', '-')
        count = SettingStore().settings.get('separate_count', 100)

        return value * count
