#!/usr/bin/env python

import xmlcurses

# initialize xmlcurses    
xmlcurses.init()

# parse xml file
xmlcurses.parse("curses.xml")

# instantiate window
win = xmlcurses.getWinByName("win_msg")

# set button actions
win.getElementByName("box").setAction("RET", lambda: win.hide())

# show the window
win.show()

