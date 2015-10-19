import sublime
import sublime_plugin


class SidebarSeparator(sublime_plugin.TextCommand):

    def run(self,edit):
        # get setting values from setting file.
        setting_values = self.GetSettingValues()

        # set separate data.
        separate_value = self.SetSeparate(setting_values)

        # create separate file.
        separate_file = sublime.active_window().new_file()

        # set buffer name.
        separate_file.set_name(separate_value)

        # set not save as separate file propertie.
        separate_file.set_scratch(True)

        # set read only propertie.
        separate_file.set_read_only(True)

    def GetSettingValues(self):
        # get separate value from setting file.
        setting_values = {}
        try:
            settings = sublime.load_settings(
                'SidebarSeparator.sublime-settings')
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
