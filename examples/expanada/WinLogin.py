#!/usr/bin/env python

from Window import Window

class WinLogin(Window):

    fldHost = None
    fldPort = None
    fldUser = None
    fldPass = None
    fldBase = None

    def onLoginPressed(self):
        # attempt login
        hostname = self.fldHost.getText()
        portnumb = self.fldPort.getText()
        username = self.fldUser.getText()
        password = self.fldPass.getText()
        database = self.fldBase.getText()
        self.con["session"].connect(hostname, portnumb, username, password, database)
        # show periods screen
        self.con["winPeriods"].show()
        # hide this screen
        self.win.hide()

    def onQuitPressed(self):
        self.win.hide()

    def __init__(self, con):
        # call Parent's constructor
        Window.__init__(self, con)
        # get fields
        self.fldHost = self.win.getElementByName("host")
        self.fldPort = self.win.getElementByName("port")
        self.fldUser = self.win.getElementByName("user")
        self.fldPass = self.win.getElementByName("pass")
        self.fldBase = self.win.getElementByName("base")
        # register handlers
        self.win.getElementByName("box").setAction("RET", lambda: self.onLoginPressed())
        self.win.getElementByName("box").setAction("ESC", lambda: self.onQuitPressed())

