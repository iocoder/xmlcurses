#!/usr/bin/env python

from Window import Window

class WinEditPeriod(Window):

    indx        = ""
    fldFirstDay = None
    fldLastDay  = None

    def onOkPressed(self):
        # collect input
        indx     = self.indx
        firstday = self.fldFirstDay.getText()
        lastday  = self.fldLastDay.getText()
        # update the element in the database
        self.con["session"].updatePeriod(indx, firstday, lastday)
        # hide this screen
        self.win.hide()

    def onCancelPressed(self):
        # hide window
        self.win.hide()

    def setData(self, indx, firstday, lastday):
        # set data before view
        self.indx = indx
        self.fldFirstDay.setText(firstday)
        self.fldLastDay.setText(lastday)

    def __init__(self, con):
        # call Parent's constructor
        Window.__init__(self, con)
        # get fields
        self.fldFirstDay = self.win.getElementByName("firstday")
        self.fldLastDay  = self.win.getElementByName("lastday" )
        # register handlers
        self.win.getElementByName("box").setAction("RET", lambda: self.onOkPressed    ())
        self.win.getElementByName("box").setAction("ESC", lambda: self.onCancelPressed())

