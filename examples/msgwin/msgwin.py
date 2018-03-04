#!/usr/bin/env python2

import xmlcurses

# initialize xmlcurses    
xmlcurses.init()

# parse xml file
xmlcurses.parse("curses.xml")

# instantiate window
win = xmlcurses.getWinByName("winmsg")

# set button actions
win.getElementByName("box").setAction("RET", lambda: win.hide())

# show the window
win.show()

