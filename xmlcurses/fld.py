#!/usr/bin/env python

class Field:
    name      = ""
    title     = ""
    text      = ""
    width     = ""
    color     = ""
    txtwin    = None
    txtbox    = None

    def draw(self, win):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # get window size
        rows, cols = win.curswin.getmaxyx()
        # get curline
        curline = win.curline
        # calculate field's title width
        titlewidth = len(self.title)+1
        # calculate textbox width
        totwidth  = cols-4-titlewidth
        textwidth = 0
        if (self.width[-1] == "%"):
            textwidth = int(self.width[:-1])*(totwidth)/100
        else:
            textwidth = min(int(self.width), totwidth)
        # find place to begin at
        x = (cols-4-textwidth-titlewidth)/2+2
        # move to line and char
        win.curswin.move(curline, x)
        # get colors
        tcolor = curses.color_pair(colors[win.color ].pairid)
        fcolor = curses.color_pair(colors[self.color].pairid)
        tflags = curses.A_BOLD
        fflags = curses.A_BOLD|curses.A_REVERSE
        # print title
        win.curswin.addstr(self.title, tcolor|tflags)
        # text window
        self.txtwin = curses.newwin(1, textwidth, curline, x+titlewidth)
        self.txtwin.bkgd('\0', fcolor|fflags)
        self.txtwin.clear()
        # insert initial val
        self.txtwin.addstr(self.text)
        # create an editable box over the window
        self.txtbox = curses.textpad.Textbox(self.txtwin)
        # done 
        return 1

    def getHeight(self):
        # only 1 line
        return 1

    def refresh(self):
        # refresh text window
        self.txtwin.refresh()

