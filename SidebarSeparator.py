import sublime
import json
import os.path
from sublime_plugin import TextCommand
from sublime_plugin import EventListener

# shared by the entire plugins.
settings = None
config = None


def plugin_loaded():
    # update settings.
    _update_settings()

    # update config.
    _update_config()

    # add settings modified listener.
    settings.add_on_change('reload', _update_settings)


def _update_config():
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

    # use global definition.
    global config

    if(config is None):
        config = _load_config()

    TabStatusStore.set_show_tab_status(get_tab_visibility_option())


def _update_settings():
    # use global definition.
    global settings

    # load settings value from setting file.
    settings = sublime.load_settings('sidebar_separator.sublime-settings')


def get_separate_value():
    # use global definition.
    global settings

    # get separate value and create separater.
    value = settings.get('separate_value', '-')
    count = settings.get('separate_count', '100')

    return value * count


def get_auto_hide_option():
    # use global definition.
    global settings

    # get auto_tab_hide option and return the flag.
    auto_hide_flag = settings.get('auto_tab_hide', True)

    return auto_hide_flag


def get_tab_visibility_option():
    # use global definition.
    global config

    return config['windows'][0]['show_tabs']


class TabControlListener(EventListener):

    def on_window_command(self, window, command, option):
        def _new_window():
            TabStatusStore.set_active_window_status()

        def _toggle_tabs(command, option):
            if(option == 'sidebar_separator' and get_auto_hide_option(
            ) and TabStatusStore.get_show_tab_status()):
                # set tab hide flag.
                TabStatusStore.set_show_tab_status(False)
                return True
            elif(not get_auto_hide_option()):
                TabStatusStore.toggle_show_tab_status()
                return True
            elif(get_auto_hide_option()):
                return False

        if(command == 'toggle_tabs'):
            if (not _toggle_tabs(command, option)):
                return ('None')
        elif(command == 'new_window'):
            _new_window()


class TabStatusStore():

    # show_tabs parameter from Session.sublime_session.
    _show_tab_status = {}

    # just before active window status.
    _active_window_status = None

    @classmethod
    def set_active_window_status(store):
        store._active_window_status = TabStatusStore.get_show_tab_status()

    @classmethod
    def get_active_window_status(store):
        return store._active_window_status

    @classmethod
    def get_show_tab_status(store):
        # get active window_id
        window_id = sublime.active_window().id()

        if(not window_id in store._show_tab_status):
            # set just before active window id.
            store._show_tab_status[window_id] = store._active_window_status

        return store._show_tab_status[window_id]

    @classmethod
    def set_show_tab_status(store, status):
        # get active window_id
        window_id = sublime.active_window().id()

        # set show_tab_status.
        store._show_tab_status[window_id] = status

    @classmethod
    def toggle_show_tab_status(store):
        # get active window_id
        window_id = sublime.active_window().id()

        store._show_tab_status[
            window_id] = not store._show_tab_status[window_id]


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
        separate_file.set_name(get_separate_value())

        # set not save as separate file propertie.
        separate_file.set_scratch(True)

        # set read only propertie.
        separate_file.set_read_only(True)

    def hide_tab_bar(self):
        # controlling the tabs when the flag is true.
        if(get_auto_hide_option() and TabStatusStore.get_show_tab_status()):

            active_window = sublime.active_window()
            active_window.run_command('toggle_tabs', 'sidebar_separator')
