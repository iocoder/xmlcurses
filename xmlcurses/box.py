#!/usr/bin/env python

class ButtonBox:

    # context
    con       = None
    # attributes
    name      = ""
    height    = "1"
    buttons   = None
    # parent
    win       = None
    # focus
    focusable = False
    # internal
    actions   = None

    def __init__(self):
        # initialize
        self.buttons = []
        self.actions = {}

    def draw(self):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # get parent window
        win    = self.win
        # get parent window size
        rows, cols = win.curswin.getmaxyx()
        # store current cursor location
        oldy, oldx = win.curswin.getyx()
        # find first line to draw the element at
        els = win.elements
        firstline = 1+sum(int(el.height) for el in els[0:els.index(self)])
        # move cursor to firstline
        win.curswin.move(firstline, 1)
        # print padding
        btnswidth = 0
        for btn in self.buttons:
            btnswidth += len(btn["key"]) + len(btn["text"]) + 2
        spaces  = " " * ((cols-2-btnswidth)//2)
        win.curswin.addstr(spaces)
        # print buttons
        for btn in self.buttons:
            # get button attributes
            key    = btn["key"]
            txt    = btn["text"]
            kcolor = curses.color_pair(colors[win.color ].pairid)
            tcolor = curses.color_pair(colors[self.color].pairid)
            flags  = curses.A_BOLD
            # print KEY:[ TEXT ]
            win.curswin.addstr(key, kcolor|flags)
            win.curswin.addstr(":", kcolor|flags)
            win.curswin.addstr(txt, tcolor|flags)
            win.curswin.addstr(" ", kcolor|flags)
            win.curswin.addstr(" ", kcolor|flags)
        # restore cursor location
        win.curswin.move(oldy, oldx)

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
        # calculate key string
        if char == 10:
            key = "RET"
        elif char == 27:
            key = "ESC"
        elif char < 256:
            key = chr(char)
        else:
            return
        # execute action
        action = None
        try:
            action = self.actions[key.lower()]
        except:
            pass
        if action != None:
            action()

    # add button
    def addButton(self, key, text):
        self.buttons.append({"key": key, "text": text})
    
    # set action
    def setAction(self, key, action):
        self.actions[key.lower()] = action

