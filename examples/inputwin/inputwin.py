#!/usr/bin/env python2

import xmlcurses

# initialize xmlcurses    
xmlcurses.init()

# parse xml file
xmlcurses.parse("curses.xml")

# get window instance
win = xmlcurses.getWinByName("wininput")

# get text fields
field1 = win.getElementByName("field1")
field2 = win.getElementByName("field2")

# set an initial value for field 2
field2.setText("initial value")

# set button actions
box = win.getElementByName("box")
box.setAction("RET", lambda: [f.setText('') for f in [field1, field2]])
box.setAction("ESC", lambda: win.hide())

# show the window
win.show()

