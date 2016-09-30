Add Separator to Open Files List in Sidebar
=====================================================

Adds a customizable separator to the open files list in Sublime Text sidebar. 

![add separate image](./view.png "add separate image.")

How to use
=====

**To add a separator**, press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>S</kbd> (in Windows or OS X) or select `Add Separate` in the right-click menu of sidebar folders.

**To remove a separator**, click `X` to the left of this separator. The same way as you would close any file.

Settings
=====
* `separate_value`: a character to be displayed as a separator (default: `-`);
* `separate_count`: number of separate characters (default: `100`).

~~~

{
   // Character used as list separator
   "separate_value": "-",
   
   // Number of separating characters
   "separate_count": 100,
   
   // If true, Sublime Text would hide tabs when you add a separator
   // To return tabs, choose View > Show Tabs in menu
   // Please enable only if you want to only to the management of the sidebar
   "auto_tab_hide": false,
}

~~~

To edit these settings, open `Preferences > Package Settings > SidebarSeparator > Settings - User`.  

License
====
This software is released under the MIT License, see [LICENSE](https://github.com/ekazyam/SidebarSeparator/blob/master/LICENSE).
