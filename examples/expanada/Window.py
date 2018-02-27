#!/usr/bin/env python

class Window():

    con = None   # context
    win = None   # xmlcurses window structure

    # constructor
    def __init__(self, con):
        self.con = con
        className = self.__class__.__name__
        self.con["xmlcurses"].parse(className + ".xml")
        self.win = self.con["xmlcurses"].getWinByName(className)

    # show window
    def show(self):
        self.win.show()

