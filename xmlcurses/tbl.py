#!/usr/bin/env python

class Table:

    # context
    con      = None
    # attributes
    name     = ""
    colnames = []
    height   = ""
    color    = ""
    # parent
    win      = None
    # focus
    focusable = False
    # internal
    selrow   = -1
    rowdata  = []

    def draw(self):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # get parent window
        win    = self.win
        # get parent window size
        rows, cols = win.curswin.getmaxyx()
        # find first line to draw the element at
        els = win.elements
        firstline = 1+sum(el.getLines() for el in els[0:els.index(self)])
        # new data inserted?
        if (self.selrow < 0 and len(self.rowdata) > 0):
            self.selrow = 0
        # data removed?
        if (self.selrow > len(self.rowdata)-1):
            self.selrow = len(self.rowdata)-1
        # get colors
        hcolor = curses.color_pair(colors[win.color ].pairid)
        rcolor = curses.color_pair(colors[self.color].pairid)
        nflags = curses.A_BOLD
        hflags = curses.A_BOLD|curses.A_REVERSE
        # draw a horizontal line
        win.curswin.hline(firstline+0, 0,      curses.ACS_LTEE,  1)
        win.curswin.hline(firstline+0, 1,      curses.ACS_HLINE, cols-2)
        win.curswin.hline(firstline+0, cols-1, curses.ACS_RTEE,  1)
        # print table titles
        colwidth = (cols-3)/len(self.colnames)
        win.curswin.move(firstline+1, 1)
        for colname in self.colnames:
            text  = ("{:^%d}"%(colwidth)).format(colname)
            win.curswin.addstr(text, hcolor|nflags)
        # dashes again
        win.curswin.hline(firstline+2, 0,      curses.ACS_LTEE,  1)
        win.curswin.hline(firstline+2, 1,      curses.ACS_HLINE, cols-2)
        win.curswin.hline(firstline+2, cols-1, curses.ACS_RTEE,  1)
        # print rows
        cur_row = 0
        for row in self.rowdata:
            # move to row line
            win.curswin.move(firstline+3+cur_row, 1)
            # initialize color
            if (cur_row == self.selrow):
                # selected row
                color = rcolor|hflags
            else:
                # normal color for other rows
                color = rcolor|nflags
            # loop over columns
            for colname in self.colnames:
                # get cell value
                cell = row[colname]
                # centerize
                text = ("{:^%d}"%(colwidth)).format(cell)
                # add cell
                win.curswin.addstr(text, color)
            # print some padding spaces
            while True:
                y, x = win.curswin.getyx()
                if (x < cols-1):
                    win.curswin.addstr(" ", color)
                else:
                    break
            # finshed one row
            cur_row = cur_row + 1

    # get table height (including header)
    def getLines(self):
        # calculate lines
        if (self.height[-1] == "%"):
            available = rows-2
            # calculate the percentage out of
            # the remaining space in the parent
            # window.
            for el in win.elements:
                if (el.getHeight() > 0):
                    available -= el.getHeight()
            lines = int(self.height[:-1])*(available)/100
            # add header
            lines += 3
        else:
            lines = int(self.height)+3
        return lines

    def setFocus(self):
        # non-focusable
        None

    def clearFocus(self):
        # non-focusable
        None

    # process keyboard input
    def keyPress(self, char):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # process key
        if (char == curses.KEY_DOWN):
            # select next row
            if (self.selrow < len(self.rowdata) - 1):
                self.selrow = self.selrow+1
        elif (char == curses.KEY_UP):
            # select previous row
            if (self.selrow > 0):
                self.selrow = self.selrow-1

    # add row to table
    def addRow(self, row):
        self.rowdata.append(row)

