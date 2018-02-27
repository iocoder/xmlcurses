#!/usr/bin/env python

from Window import Window

class WinAddPeriod(Window):

    fldFirstDay = None
    fldLastDay  = None

    def onOkPressed(self):
        # collect input
        firstday = self.fldFirstDay.getText()
        lastday  = self.fldLastDay.getText()
        # add element to database
        self.con["session"].addPeriod(firstday, lastday)
        # hide this screen
        self.win.hide()

    def onCancelPressed(self):
        self.win.hide()

    def __init__(self, con):
        # call Parent's constructor
        Window.__init__(self, con)
        # get fields
        self.fldFirstDay = self.win.getElementByName("firstday")
        self.fldLastDay  = self.win.getElementByName("lastday" )
        # register handlers
        self.win.getElementByName("box").setAction("RET", lambda: self.onOkPressed    ())
        self.win.getElementByName("box").setAction("ESC", lambda: self.onCancelPressed())

