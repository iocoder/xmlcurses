#!/usr/bin/env python

class Table:

    # context
    con       = None
    # attributes
    name      = ""
    colnames  = None
    height    = ""
    color     = ""
    # parent
    win       = None
    # focus
    focusable = False
    # internal
    selrow    = -1
    firstrow  = 0
    rowdata   = None
    drawn     = False

    def __init__(self):
        # initialize
        self.colnames = []
        self.rowdata  = []

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
        firstline = 1+sum(int(el.height) for el in els[0:els.index(self)])
        # get colors
        hcolor = curses.color_pair(colors[win.color ].pairid)
        rcolor = curses.color_pair(colors[self.color].pairid)
        nflags = curses.A_BOLD
        hflags = curses.A_BOLD|curses.A_REVERSE
        # get height
        height = int(self.height)
        if height < 5:
            height = 5
        # draw a horizontal line
        win.curswin.hline(firstline+0, 0,      curses.ACS_LTEE,  1)
        win.curswin.hline(firstline+0, 1,      curses.ACS_HLINE, cols-2)
        win.curswin.hline(firstline+0, cols-1, curses.ACS_RTEE,  1)
        # print table titles
        colwidth = (cols-3)//len(self.colnames)
        win.curswin.move(firstline+1, 1)
        for colname in self.colnames:
            text  = ("{:^%d}"%(colwidth)).format(colname)
            win.curswin.addstr(text, hcolor|nflags)
        # dashes again
        win.curswin.hline(firstline+2, 0,      curses.ACS_LTEE,  1)
        win.curswin.hline(firstline+2, 1,      curses.ACS_HLINE, cols-2)
        win.curswin.hline(firstline+2, cols-1, curses.ACS_RTEE,  1)
        # find how many rows to draw
        firstrow  = self.firstrow
        winsize   = height-4
        lastrow   = min(firstrow+winsize,len(self.rowdata))
        sparerows = firstrow+winsize-lastrow
        # print rows
        cur_row = 0
        for indx in range(firstrow, lastrow):
            # fetch row
            row = self.rowdata[indx]
            # move to row line
            win.curswin.move(firstline+3+cur_row, 1)
            # initialize color
            if (indx == self.selrow):
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
        # draw empty lines
        for i in range(0, sparerows):
            win.curswin.move(firstline+3+cur_row+i, 1)
            win.curswin.addstr(" " * (cols-2))
        # calculate scroll line parameters
        scrollline = firstline+3+cur_row+sparerows
        if (len(self.rowdata) == 0):
            before = 0
            shown  = cols-2
            after  = 0
        else:
            before = firstrow*(cols-2)//len(self.rowdata)
            shown  = (lastrow-firstrow)*(cols-2)//len(self.rowdata)
            if (shown < 3):
                shown = 3
                if (before+shown > cols-2):
                    before = cols-2-shown
            after  = cols-2-shown-before
            if lastrow == len(self.rowdata):
                shown += after
                after = 0   
        # print before
        win.curswin.hline(scrollline,  0,                    curses.ACS_LTEE,  1)
        win.curswin.hline(scrollline,  1,                    curses.ACS_HLINE, before)
        # print the shown part
        if (shown == cols-2):
            win.curswin.hline(scrollline,  1+before,         curses.ACS_HLINE, cols-2)    
        else:
            win.curswin.addstr(scrollline, 1+before, "[" + "="*(shown-2) + "]")        
        # print after
        win.curswin.hline(scrollline,  1+before+shown,       curses.ACS_HLINE, after)
        win.curswin.hline(scrollline,  1+before+shown+after, curses.ACS_RTEE,  1)
        # done
        self.drawn = True

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
        # get height
        height = int(self.height)
        if (height < 5):
            height = 5
        # process key
        if (char == curses.KEY_DOWN):
            # select next row
            if (self.selrow < len(self.rowdata) - 1):
                self.selrow = self.selrow+1
                # update window boundaries
                if (self.selrow >= self.firstrow+height-4):
                    self.firstrow += 1
                # redraw window if needed
                if self.drawn:
                    self.win.redraw()
        elif (char == curses.KEY_UP):
            # select previous row
            if (self.selrow > 0):
                self.selrow = self.selrow-1
                # update window boundaries
                if (self.selrow < self.firstrow):
                    self.firstrow -= 1
                # redraw window if needed
                if self.drawn:
                    self.win.redraw()

    # get current selected row
    def getSelRowIndex(self):
        return self.selrow

    # set current selected row
    def setSelRowIndex(self, selrow):
        # update selrow
        self.selrow = selrow
        # get height
        height = int(self.height)
        if (height < 5):
            height = 5
        # update window boundaries
        if (self.selrow >= self.firstrow+height-4):
            self.firstrow += 1
        if (self.selrow < self.firstrow):
            self.firstrow -= 1
        # redraw window if needed
        if self.drawn:
            self.win.redraw()

    # add row to table
    def addRow(self, row):
        # append
        self.rowdata.append(row)
        # update selrow
        if (self.selrow < 0):
            self.selrow = 0
        # redraw window if needed
        if self.drawn:
            self.win.redraw()

    # update row data
    def setRow(self, indx, row):
        # update
        self.rowdata[indx] = row
        # redraw window if needed
        if self.drawn:
            self.win.redraw()

    # get row data
    def getRow(self, indx):
        # return the row
        return self.rowdata[indx]

    # delete row at index
    def delRow(self, indx):
        # index is less than zero?
        if indx < 0:
            return
        # delete a row
        self.rowdata.remove(self.rowdata[indx])
        # update window boundaries
        if (self.selrow > 0 and self.selrow == self.firstrow):
            self.firstrow -= 1
        # update selrow
        if (self.selrow > len(self.rowdata)-1):
            self.selrow = len(self.rowdata)-1
        # redraw window if needed
        if self.drawn:
            self.win.redraw()

    # delete all rows
    def delAllRows(self):
        # clear the whole list
        self.rowdata = []
        # update window boundaries
        self.firstrow = 0
        # update selrow
        self.selrow = -1
        # redraw window if needed
        if self.drawn:
            self.win.redraw()

