#!/usr/bin/env python

import xmlcurses

# initialize xmlcurses
xmlcurses.init()

# parse xml file
xmlcurses.parse("curses.xml")

# get window instance
win = xmlcurses.getWinByName("win_table")

# get the table
tbl = win.getElementByName("tbl")
tbl.addRow({"A": "000", "B": "001", "C": "002", "D": "003"})
tbl.addRow({"A": "010", "B": "011", "C": "012", "D": "013"})
tbl.addRow({"A": "020", "B": "021", "C": "022", "D": "023"})

# set button action
box = win.getElementByName("box")
box.getButtonByName("ok").setAction(lambda win: win.hide())
box.getButtonByName("ca").setAction(lambda win: win.hide())

# show the window
win.show()

