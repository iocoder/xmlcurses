#!/usr/bin/env python

import xmlcurses

# initialize xmlcurses    
xmlcurses.init("curses.xml")

# set actions for OK and CANCEL buttons
xmlcurses.setAction("act_ok", lambda win: win.hide())
xmlcurses.setAction("act_ca", lambda win: win.hide())

# instantiate window
win = xmlcurses.newWinByName("win_msg")

# show the window
win.show()

# finalize
xmlcurses.close()

