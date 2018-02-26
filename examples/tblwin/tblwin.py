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
row = {"A": "000", "B": "001", "C": "002", "D": "003"}
tbl.addRow(row)
tbl.addRow(row)
tbl.addRow(row)

# set button action
box = win.getElementByName("box")
box.setAction("A", lambda win: tbl.addRow(row))
box.setAction("D", lambda win: tbl.delRow(tbl.getSelRowIndex()))
box.setAction("Q", lambda win: win.hide())

# show the window
win.show()

