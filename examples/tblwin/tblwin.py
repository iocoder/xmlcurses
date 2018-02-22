#!/usr/bin/env python

import xmlcurses

def func1(win):
    win.hide()
    
def func2(win):
    win.hide()
    
xmlcurses.init("curses.xml")
xmlcurses.addAction("func1", func1)
xmlcurses.addAction("func2", func2)

# instantiate window
win = xmlcurses.newWinByName("win_table")
row = {"A": "YES", "B": "No", "C": "HEY", "D": "YOU"}
win.addRow(row)
win.addRow(row)
win.addRow(row)

win.show()

xmlcurses.term()



