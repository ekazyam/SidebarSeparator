Add Separater File in Open Files List
=====================================================
Add an empty file to open files list.
It'll add a hyphen in the standard.

![add separate image](./view.png "add separate image.")

Usage
=====
Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>S</kbd> or select `Add Separate` in the right-click menu on folders in the sidebar.

Config
=====
separate value indicates the character to be displayed as a separator.
separate_count indicates the number of separate characters.
~~~

{
   // Designation of separate character.
   "separate_value": "-",
   // The number of separate characters.
   "separate_count": 100,
   // Forced hidden if tab that specifies the true.
   "auto_tab_hide": true,
}

~~~

License
====
This software is released under the MIT License, see LICENSE.
