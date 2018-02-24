#!/usr/bin/env python

import xmlcurses

# initialize xmlcurses
xmlcurses.init()

# parse xml file
xmlcurses.parse("curses.xml")

# set actions for OK and CANCEL buttons
#xmlcurses.setAction("act_ok", lambda win: win.hide())
#xmlcurses.setAction("act_ca", lambda win: win.hide())

# get window instance
win = xmlcurses.getWinByName("win_table")

# get the table
tbl = win.getElementByName("tbl")

# fill table
row = {"A": "YES", "B": "No", "C": "HEY", "D": "YOU"}
tbl.addRow(row)
tbl.addRow(row)
tbl.addRow(row)

# show the window
win.show()

