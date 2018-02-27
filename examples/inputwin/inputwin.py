#!/usr/bin/env python

import xmlcurses

# initialize xmlcurses    
xmlcurses.init()

# parse xml file
xmlcurses.parse("curses.xml")

# get window instance
win = xmlcurses.getWinByName("win_input")

# get text fields
field1 = win.getElementByName("field1")
field2 = win.getElementByName("field2")

# put initial value for field 2
field2.setText("initial value")

# set button actions
box = win.getElementByName("box")
box.setAction("RET", lambda: [f.setText('') for f in [field1, field2]])
box.setAction("ESC", lambda: win.hide())

# show the window
win.show()

