#!/usr/bin/env python

class Field:

    # context
    con       = None
    # attributes
    name      = ""
    height    = "1"
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
    cursor    = (0, 0)

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
        # calculate field's title width
        titlewidth = len(self.title)+1
        # calculate textbox width
        totwidth  = cols-4-titlewidth
        textwidth = 0
        if (self.width[-1] == "%"):
            textwidth = int(self.width[:-1])*(totwidth)//100
        else:
            textwidth = min(int(self.width), totwidth)
        # find screen col to begin at
        x = (cols-4-textwidth-titlewidth)//2+2
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

    def refresh(self):
        # refresh subwindows
        self.txtwin.refresh()

    def setFocus(self):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # show cursor 
        curses.curs_set(1)
        # restore cursor location
        self.txtwin.move(self.cursor[0], self.cursor[1])
        # refresh textbox
        self.txtwin.refresh()
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
            # store cursor location
            self.cursor = self.txtwin.getyx()
            # refresh the curses window
            self.txtwin.refresh()
            # update text attribute
            self.text = self.txtbox.gather().strip()

    # set text
    def setText(self, text):
        # set text attribute
        self.text = text
        # already drawn?
        if self.txtwin != None:
            # clear text window
            self.txtwin.clear()
            # move cursor
            self.cursor = (0, 0)
            # insert text into window
            self.txtwin.addstr(self.text)
            # refresh parent window
            self.win.redraw()

    # get text
    def getText(self):
        # return text attribute
        return self.text

