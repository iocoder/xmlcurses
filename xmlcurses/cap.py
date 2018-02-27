#!/usr/bin/env python

class Caption:

    # context
    con       = None
    # attributes
    name      = ""
    height    = "1"
    text      = ""
    align     = ""
    color     = ""
    # parent
    win       = None
    # focus
    focusable = False

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
        # move cursor to firstline
        win.curswin.move(firstline, 1)
        # get caption text
        align = {"left":"<", "center":"^"}[self.align]
        text  = ("{:%c%d}"%(align,cols-2)).format(self.text)
        # get caption color
        color = curses.color_pair(colors[self.color].pairid)
        flags = curses.A_BOLD
        # print the caption
        win.curswin.addstr(text, color|flags)

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
        # do nothing
        pass
        
