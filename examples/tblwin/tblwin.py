#!/usr/bin/env python

import xmlcurses

# generate numbers
seq = 0
def gen_num():
   global seq
   seq += 1
   return "%03d" % seq 

# generate row
def gen_row():
    return {"A": gen_num(), "B": gen_num(), 
            "C": gen_num(), "D": gen_num()}

# initialize xmlcurses
xmlcurses.init()

# parse xml file
xmlcurses.parse("curses.xml")

# get window instance
win = xmlcurses.getWinByName("win_table")

# get the table
tbl = win.getElementByName("tbl")
tbl.addRow(gen_row())
tbl.addRow(gen_row())
tbl.addRow(gen_row())

# set button action
box = win.getElementByName("box")
box.setAction("A", lambda: tbl.addRow(gen_row()))
box.setAction("D", lambda: tbl.delRow(tbl.getSelRowIndex()))
box.setAction("Q", lambda: win.hide())

# show the window
win.show()

