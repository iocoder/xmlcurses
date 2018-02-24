#!/usr/bin/env python

class Caption:
    con       = None
    name      = ""
    text      = ""
    align     = ""
    color     = ""

    def draw(self, win):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # get window size
        rows, cols = win.curswin.getmaxyx()
        # get caption parameters
        line  = win.curline
        align = {"left":"<", "center":"^"}[self.align]
        text  = ("{:%c%d}"%(align,cols-2)).format(self.text)
        color = curses.color_pair(colors[self.color].pairid)
        flags = curses.A_BOLD
        # print the title
        win.curswin.addstr(line, 1, text, color|flags)
        # done
        return 1

    def getHeight(self):
        # only 1 line
        return 1

    def refresh(self):
        # no sub-windows to refresh
        None

