#!/usr/bin/env python

from Window import Window

class WinTransacts(Window):

    tblTransacts = None
    firstday     = ""
    lastday      = ""

    def setPeriod(self, firstday, lastday):
        # set selected period of time
        self.firstday = firstday
        self.lastday  = lastday

    def syncTable(self):
        # clear table
        self.tblTransacts.delAllRows()
        # get data from database
        allrows = self.con["session"].getAllTransacts(self.firstday, self.lastday)
        # add all rows
        for row in allrows:
            self.tblTransacts.addRow(row)        

    def onAddPressed(self):
        # show add-transact window
        self.con["winAddTransact"].show()
        # synchronize local table with database
        self.syncTable()

    def onEditPressed(self):
        # get selected row index
        selRow = self.tblTransacts.getSelRowIndex()
        # fetch row data
        row = self.tblTransacts.getRow(selRow)
        # update edit-transact window
        self.con["winEditTransact"].setData(row["ID"], row["DAY"], row["NAME"], row["CARD"], row["AMNT"])
        # show edit-transact window
        self.con["winEditTransact"].show()
        # fetch edited element from database
        row = self.con["session"].getTransact(row["ID"])
        # updat row in table
        self.tblTransacts.setRow(selRow, row)

    def onDelPressed(self):
        # get selected row index
        selRow = self.tblTransacts.getSelRowIndex()
        # fetch row data
        row = self.tblTransacts.getRow(selRow)
        # delete the row
        row = self.con["session"].delTransact(row["ID"])
        # updat row in table
        self.tblTransacts.delRow(selRow)

    def onQuitPressed(self):
        # hide this window
        self.win.hide()

    def __init__(self, con):
        # call Parent's constructor
        Window.__init__(self, con)
        # get table
        self.tblTransacts = self.win.getElementByName("tbl")
        # register handlers
        self.win.getElementByName("box").setAction("A", lambda: self.onAddPressed())
        self.win.getElementByName("box").setAction("E", lambda: self.onEditPressed())
        self.win.getElementByName("box").setAction("D", lambda: self.onDelPressed())
        self.win.getElementByName("box").setAction("Q", lambda: self.onQuitPressed())

    def show(self):
        # initialize content
        self.syncTable()
        # call parent's show method
        Window.show(self)

