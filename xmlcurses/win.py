#!/usr/bin/env python

class Window:

    # context
    con        = None    # runtime context information
    # attributes
    name       = ""      # window XML identifier
    width      = ""      # window XML width
    height     = ""      # window XML height
    style      = ""      # window XML style
    color      = ""      # window color
    elements   = []      # window elements in order
    # internal
    hideFlag   = False   # To be hidden after action execution
    curline    = 1       # current line to draw the next element
    curswin    = None    # pointer to curses' window structure

    # show window
    def show(self):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # translate window color
        wcolor = curses.color_pair(colors[self.color].pairid)
        wflags = curses.A_BOLD
        # get screen dimensions from curses module
        totlines = curses.LINES
        totcols  = curses.COLS
        # initialize window dimensions
        winx = 0
        winy = 0
        cols = 0
        rows = 0
        # read width
        if (self.width[-1] == "%"):
            cols = int(self.width[:-1])*(totcols)/100
        else:
            cols = int(self.width)
        # read height
        if (self.height[-1] == "%"):
            rows = int(self.height[:-1])*(totlines)/100
        else:
            rows = int(self.height)
        # calculate x
        winx = (totcols-cols)/2
        # calculate y
        winy = (totlines-rows)/2
        # create window
        self.curswin = curses.newwin(rows, cols, winy, winx)
        # find focusable elements
        focusable = []
        focusid   = -1
        for element in self.elements:
            if element.__class__.__name__ in ["Table", "Field"]:
                focusable.append(element)
                focusid = 0        
        # clear window
        self.curswin.clear()   
        # hide cursor by default
        curses.curs_set(0)
        # draw border
        self.curswin.border()
        # enable keypad
        self.curswin.keypad(1)
        # set attribute color
        self.curswin.bkgd('\0', wcolor|wflags)
        # reset curline attribute
        self.curline = 1
        # draw elements
        for element in self.elements:
            element.draw()
        # refresh window
        self.curswin.refresh()
        # any focusable element?
        focusable = []
        for element in self.elements:
            if element.focusable:
                focusable.append(element)
        if len(focusable) > 0:
            curfocus = 0
            focusable[curfocus].setFocus()
        # clear hide attribute
        self.hideFlag = False
        # process input
        while not self.hideFlag:
            # wait for keyboard input
            char = self.curswin.getch()
            # process keyboard input
            for element in self.elements:
                element.keyPress(char)
            # manipulate focus
            if len(focusable) > 0:
                if char == 9:
                    # get next focusable element
                    focusable[curfocus].clearFocus()
                    curfocus = (curfocus + 1) % len(focusable)
                    focusable[curfocus].setFocus()
                elif char == curses.KEY_BTAB:
                    # get prev focusable element
                    focusable[curfocus].clearFocus()
                    curfocus = (curfocus - 1) % len(focusable)
                    focusable[curfocus].setFocus()
                else:
                    # reserve the focus
                    focusable[curfocus].setFocus()
        # clear focus
        if len(focusable) > 0:
            focusable[curfocus].clearFocus()

    # hide window
    def hide(self):
        self.hideFlag = True

    # get sub-element by name
    def getElementByName(self, name):
        for el in self.elements:
            if (el.name == name):
                return el
        return None

    # add element
    def addElement(self, element):
        self.elements.append(element)
        element.win = self

