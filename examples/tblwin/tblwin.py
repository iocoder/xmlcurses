#!/usr/bin/env python2

import xmlcurses

# generate numbers
seq = 0
def genNum():
   global seq
   seq += 1
   return "%03d" % seq 

# generate row
def genRow():
    return {"A": genNum(), "B": genNum(), 
            "C": genNum(), "D": genNum()}

# initialize xmlcurses
xmlcurses.init()

# parse xml file
xmlcurses.parse("curses.xml")

# get window instance
win = xmlcurses.getWinByName("wintable")

# add some rows to the table
tbl = win.getElementByName("tbl")
tbl.addRow(genRow())
tbl.addRow(genRow())
tbl.addRow(genRow())

# set button action
box = win.getElementByName("box")
box.setAction("A", lambda: tbl.addRow(genRow()))
box.setAction("D", lambda: tbl.delRow(tbl.getSelRowIndex()))
box.setAction("Q", lambda: win.hide())

# show the window
win.show()

