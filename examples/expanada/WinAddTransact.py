#!/usr/bin/env python

from Window import Window

class WinAddTransact(Window):

    fldDay  = None
    fldName = None
    fldCard = None
    fldAmnt = None

    def onOkPressed(self):
        # collect input
        day  = self.fldDay.getText()
        name = self.fldName.getText()
        card = self.fldCard.getText()
        amnt = self.fldAmnt.getText()
        # add element to database
        self.con["session"].addTransact(day, name, card, amnt)
        # hide this screen
        self.win.hide()

    def onCancelPressed(self):
        self.win.hide()

    def __init__(self, con):
        # call Parent's constructor
        Window.__init__(self, con)
        # get fields
        self.fldDay  = self.win.getElementByName("day" )
        self.fldName = self.win.getElementByName("name")
        self.fldCard = self.win.getElementByName("card")
        self.fldAmnt = self.win.getElementByName("amnt")
        # register handlers
        self.win.getElementByName("box").setAction("RET", lambda: self.onOkPressed    ())
        self.win.getElementByName("box").setAction("ESC", lambda: self.onCancelPressed())

