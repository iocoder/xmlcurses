#!/usr/bin/env python

from Window import Window

class WinPeriods(Window):

    tblPeriods = None

    def syncTable(self):
        # clear table
        self.tblPeriods.delAllRows()
        # get data from database
        allrows = self.con["session"].getAllPeriods()
        # add all rows
        for row in allrows:
            self.tblPeriods.addRow(row)        

    def onSelPressed(self):
        # get selected row index
        selRow = self.tblPeriods.getSelRowIndex()
        # fetch row data
        row = self.tblPeriods.getRow(selRow)
        # update transaction window with selected period
        self.con["winTransacts"].setPeriod(row["FIRSTDAY"], row["LASTDAY"])
        # show transaction window
        self.con["winTransacts"].show()
        # quit
        self.win.hide()

    def onAddPressed(self):
        # show add-period window
        self.con["winAddPeriod"].show()
        # synchronize local table with database
        self.syncTable()
        # redraw window
        self.win.redraw()

    def onEditPressed(self):
        # get selected row index
        selRow = self.tblPeriods.getSelRowIndex()
        # fetch row data
        row = self.tblPeriods.getRow(selRow)
        # update edit-period window
        self.con["winEditPeriod"].setData(row["ID"], row["FIRSTDAY"], row["LASTDAY"])
        # show edit-period window
        self.con["winEditPeriod"].show()
        # fetch edited element from database
        row = self.con["session"].getPeriod(row["ID"])
        # updat row in table
        self.tblPeriods.setRow(selRow, row)
        # redraw window
        self.win.redraw()

    def onDelPressed(self):
        # get selected row index
        selRow = self.tblPeriods.getSelRowIndex()
        # fetch row data
        row = self.tblPeriods.getRow(selRow)
        # delete the row
        row = self.con["session"].delPeriod(row["ID"])
        # updat row in table
        self.tblPeriods.delRow(selRow)
        # redraw window
        self.win.redraw()

    def onQuitPressed(self):
        # hide this window
        self.win.hide()

    def __init__(self, con):
        # call Parent's constructor
        Window.__init__(self, con)
        # get table
        self.tblPeriods = self.win.getElementByName("tbl")
        # register handlers
        self.win.getElementByName("box").setAction("S", lambda: self.onSelPressed())
        self.win.getElementByName("box").setAction("A", lambda: self.onAddPressed())
        self.win.getElementByName("box").setAction("E", lambda: self.onEditPressed())
        self.win.getElementByName("box").setAction("D", lambda: self.onDelPressed())
        self.win.getElementByName("box").setAction("Q", lambda: self.onQuitPressed())

    def show(self):
        # initialize content
        self.syncTable()
        # call parent's show method
        Window.show(self)

