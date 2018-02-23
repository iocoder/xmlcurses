#!/usr/bin/env python

import xmlcurses
    
# initialize xmlcurses
xmlcurses.init("curses.xml")

# set actions for OK and CANCEL buttons
xmlcurses.setAction("act_ok", lambda win: win.hide())
xmlcurses.setAction("act_ca", lambda win: win.hide())

# instantiate window
win = xmlcurses.newWinByName("win_table")

# fill table
row = {"A": "YES", "B": "No", "C": "HEY", "D": "YOU"}
win.addRow(row)
win.addRow(row)
win.addRow(row)

# show the window
win.show()

# exit
xmlcurses.close()

