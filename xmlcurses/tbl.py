#!/usr/bin/env python

class Table:

    # context
    con       = None
    # attributes
    name      = ""
    colnames  = []
    height    = ""
    color     = ""
    # parent
    win       = None
    # focus
    focusable = False
    # internal
    drawn     = False
    selrow    = -1
    rowdata   = []

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
        # draw empty lines for next lines
        for i in range(0, self.getLines()-3-cur_row):
            win.curswin.move(firstline+3+cur_row+i, 1)
            win.curswin.addstr(" " * (cols-2))
            
        # done
        self.drawn = True

    # get table height (including header)
    def getLines(self):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # get parent window
        win    = self.win
        # get parent window size
        rows, cols = win.curswin.getmaxyx()
        # calculate lines
        if (self.height[-1] == "%"):
            available = rows-2
            # calculate the percentage using
            # parent window size
            lines = int(self.height[:-1])*(available)/100
            # add header
            lines += 3
        else:
            lines = int(self.height)+3
        return lines

    def refresh(self):
        # refresh subwindows
        pass

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
        # redraw if needed
        if self.drawn:
            self.draw()

    # get current selected row
    def getSelRowIndex(self):
        return self.selrow

    # add row to table
    def addRow(self, row):
        # append
        self.rowdata.append(row)
        # update selrow
        if (self.selrow < 0):
            self.selrow = 0
        # redraw if needed
        if self.drawn:
            self.draw()

    # update row data
    def setRow(self, indx, row):
        # update
        self.rowdata[indx] = row
        # redraw if needed
        if self.drawn:
            self.draw()

    # get row data
    def getRow(self, indx):
        # return the row
        return self.rowdata[indx]

    # delete row at index
    def delRow(self, indx):
        # delete a row
        self.rowdata.remove(self.rowdata[indx])
        # update selrow
        if (self.selrow > len(self.rowdata)-1):
            self.selrow = len(self.rowdata)-1
        # redraw if needed
        if self.drawn:
            self.draw()

