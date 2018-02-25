#!/usr/bin/env python

class Field:

    # context
    con       = None
    # attributes
    name      = ""
    title     = ""
    text      = ""
    width     = ""
    color     = ""
    # parent
    win       = None
    # focus
    focusable = True
    # internal
    txtwin    = None
    txtbox    = None
    onFocus   = False

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
        # calculate field's title width
        titlewidth = len(self.title)+1
        # calculate textbox width
        totwidth  = cols-4-titlewidth
        textwidth = 0
        if (self.width[-1] == "%"):
            textwidth = int(self.width[:-1])*(totwidth)/100
        else:
            textwidth = min(int(self.width), totwidth)
        # find screen col to begin at
        x = (cols-4-textwidth-titlewidth)/2+2
        # move to line and char
        win.curswin.move(firstline, x)
        # get colors
        tcolor = curses.color_pair(colors[win.color ].pairid)
        fcolor = curses.color_pair(colors[self.color].pairid)
        tflags = curses.A_BOLD
        fflags = curses.A_BOLD|curses.A_REVERSE
        # print title
        win.curswin.addstr(self.title, tcolor|tflags)
        # text window
        self.txtwin = win.curswin.derwin(1, textwidth, firstline, x+titlewidth)
        self.txtwin.bkgd('\0', fcolor|fflags)
        self.txtwin.clear()
        # insert initial val
        self.txtwin.addstr(self.text)
        # create an editable box over the window
        self.txtbox = curses.textpad.Textbox(self.txtwin)

    def getLines(self):
        # only 1 line
        return 1

    def setFocus(self):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # show cursor 
        curses.curs_set(1)
        # refresh textbox
        self.txtwin.refresh()
        # update cursor location
        self.txtwin.cursyncup()
        # set onFocus flag
        self.onFocus = True

    def clearFocus(self):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # hide cursor
        curses.curs_set(0)
        # update text attribute
        self.text = self.txtbox.gather().strip()
        # clear onFocus flag
        self.onFocus = False

    # process keyboard input
    def keyPress(self, char):
        if self.onFocus == True:
            # perform key stroke
            self.txtbox.do_command(char)
            # refresh the curses window
            self.txtwin.refresh()

    # set text
    def setText(self, text):
        # set text attribute
        self.text = text
        # clear txtwin content
        self.txtwin.clear()
        # update txtwin content
        self.txtwin.addstr(text)
        # refresh textbox
        self.txtwin.refresh()

    # get text
    def getText(self):
        # update text attribute
        self.text = self.txtbox.gather().strip()
        # return text attribute
        return self.text

