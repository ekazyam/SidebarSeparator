import sublime
import sublime_plugin


class SidebarSeparator(sublime_plugin.TextCommand):

    def run(self, edit):
        # set writing point at separate file.
        start_point = 0

        # get settign values from setting file.
        setting_values = self.GetSettingValues()

        # set separate data.
        separate_value = self.SetSeparate(setting_values)

        # create separate file.
        separate_file = sublime.active_window().new_file()

        # set not save as separate file propertie.
        separate_file.set_scratch(True)

        # write separate data in dummy file.
        separate_file.insert(edit, start_point, separate_value)

    def GetSettingValues(self):
        # get separate value from setting file.
        setting_values = {}
        try:
            settings = sublime.load_settings('SidebarSeparator.sublime-settings')
            setting_values["separate_value"] = settings.get(
                'separate_value', '-')
            setting_values["separate_count"] = settings.get(
                'separate_count', 100)
        except:
            pass
        return setting_values

    def SetSeparate(self, setting_values):
        # set separate value
        return setting_values["separate_value"] * setting_values["separate_count"]
