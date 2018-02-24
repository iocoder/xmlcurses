#!/usr/bin/env python

class ButtonBox:
    name    = ""
    buttons = []
    win     = None

    def draw(self, win):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # get window size
        rows, cols = win.curswin.getmaxyx()
        # move cursor to curline
        win.curswin.move(win.curline, 1)
        # print padding
        btnswidth = 0
        for btn in self.buttons:
            btnswidth += len(btn.key) + len(btn.text) + 2
        spaces  = " " * ((cols-btnswidth)/2)
        win.curswin.addstr(spaces)
        # print buttons
        for btn in self.buttons:
            # get button attributes
            key    = btn.key
            txt    = btn.text
            kcolor = curses.color_pair(colors[win.color].pairid)
            tcolor = curses.color_pair(colors[btn.color].pairid)
            flags  = curses.A_BOLD
            # print KEY:[ TEXT ]
            win.curswin.addstr(key, kcolor|flags)
            win.curswin.addstr(":", kcolor|flags)
            win.curswin.addstr(txt, tcolor|flags)
            win.curswin.addstr(" ", kcolor|flags)
            win.curswin.addstr(" ", kcolor|flags)
        # done
        return 1

    def getHeight(self):
        # only 1 line
        return 1

    def refresh(self):
        # no sub-windows to refresh
        None

