#!/usr/bin/env python

from Window import Window

class WinEditTransact(Window):

    indx    = ""
    fldDay  = None
    fldName = None
    fldCard = None
    fldAmnt = None

    def onOkPressed(self):
        # collect input
        indx = self.indx
        day  = self.fldDay.getText()
        name = self.fldName.getText()
        card = self.fldCard.getText()
        amnt = self.fldAmnt.getText()
        # update the element in the database
        self.con["session"].updateTransact(indx, day, name, card, amnt)
        # hide this screen
        self.win.hide()

    def onCancelPressed(self):
        # hide window
        self.win.hide()

    def setData(self, indx, day, name, card, amnt):
        # set data before view
        self.indx = indx
        self.fldDay.setText(day)
        self.fldName.setText(name)
        self.fldCard.setText(card)
        self.fldAmnt.setText(amnt)

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

