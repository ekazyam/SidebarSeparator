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


class Listener(EventListener):

    def on_window_command(self, window, command, option):
        # toggle_tabs command except it does not control.
        print('コマンド：', command, '/オプション：', option,
              '/ウインドウ：', window, '/セルフ：', self)


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
        if(get_auto_hide_option()):
            sublime.active_window().run_command('toggle_tabs', 'sidebar_separator')
