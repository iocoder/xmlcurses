#!/usr/bin/env python

class Table:
    con      = None
    name     = ""
    colnames = []
    height   = ""
    color    = ""
    lines    = -4
    selrow   = -1
    rowdata  = []

    def draw(self, win):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # get window size
        rows, cols = win.curswin.getmaxyx()
        # get window curline
        curline = win.curline
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
            # reserve 3 lines for header
            lines -= 3
            # too small?
            if (lines < 1):
                lines = 1
        else:
            lines = int(self.height)
        self.lines = lines
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
        # horizontal line
        win.curswin.hline(curline+0, 0,      curses.ACS_LTEE,  1)
        win.curswin.hline(curline+0, 1,      curses.ACS_HLINE, cols-2)
        win.curswin.hline(curline+0, cols-1, curses.ACS_RTEE,  1)
        # print table titles
        colwidth = (cols-3)/len(self.colnames)
        win.curswin.move(curline+1, 1)
        for colname in self.colnames:
            text  = ("{:^%d}"%(colwidth)).format(colname)
            win.curswin.addstr(text, hcolor|nflags)
        # dashes again
        win.curswin.hline(curline+2, 0,      curses.ACS_LTEE,  1)
        win.curswin.hline(curline+2, 1,      curses.ACS_HLINE, cols-2)
        win.curswin.hline(curline+2, cols-1, curses.ACS_RTEE,  1)
        # print rows
        cur_row = 0
        for row in self.rowdata:
            # move to row line
            win.curswin.move(curline+3+cur_row, 1)
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
        # done
        return self.lines + 3

    # get table height (including header)
    def getHeight(self):
        return self.lines + 3

    # used by win.show()
    def refresh(self):
        # no sub-windows to refresh
        None
    # add row to table
    def addRow(self, row):
        self.rowdata.append(row)

