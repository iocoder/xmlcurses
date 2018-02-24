#!/usr/bin/env python

from curses.textpad import Textbox, rectangle
from utils import center

class Window:
    con        = None    # runtime context information
    name       = ""      # window XML identifier
    width      = ""      # window XML width
    height     = ""      # window XML height
    style      = ""      # window XML style
    color      = ""      # window color    
    elements   = []      # window elements in order
    hideFlag   = False   # To be hidden after action execution
    curline    = 1       # current line to draw the next element
    curswin    = None    # pointer to curses' window structure

    """
    # refresh display
    curswin.refresh()
    # process keyboard input
    curswin.keypad(1)
    char = curswin.getkey()
    if (char == "KEY_DOWN"):
        # select next row
        if (self.selrow < len(self.tbldata) - 1):
            self.selrow = self.selrow+1
    elif (char == "KEY_UP"):
        # select previous row
        if (self.selrow > 0):
            self.selrow = self.selrow-1
    else:
        # execute button
        for btn in self.buttons:
            if ((btn.key == "RET" and char == chr(10)) or
                (btn.key == "ESC" and char == chr(27)) or
                btn.key == char.capitalize()):
                actions[btn.action](self)

    # print fields area
            # let the user edit first textbox       
            txtwins[cur_box].refresh()
            txtboxes[cur_box].edit(
                lambda ch: 
                    [setattr(self,'edit_cmd', ch),
                     7 if ch in [10, 27, 259, 258] else ch][-1]);
            # process command:
            if (self.edit_cmd == 259):
                # key up
                if (cur_box > 0):
                    cur_box = cur_box - 1
            elif (self.edit_cmd == 258):
                # key down
                if (cur_box < len(txtboxes)-1):
                    cur_box = cur_box + 1
            else:
                # execute button
                for btn in self.buttons:
                    if ((btn.key == "RET" and self.edit_cmd == 10) or
                        (btn.key == "ESC" and self.edit_cmd == 27)):
                        actions[btn.action](self)
        # collect inputs
        cur_box = 0
        for field in self.fields:
            field.text = txtboxes[cur_box].gather().strip()
        # hide cursor    
        curses.curs_set(0)
    """

    def show(self):
        # get context variables
        curses = self.con.curses
        wins   = self.con.wins
        colors = self.con.colors
        # clear hide attribute
        self.hideFlag = False
        # reset curline attribute
        self.curline = 1
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
        # draw border
        self.curswin.border()
        # enable keypad
        self.curswin.keypad(1)
        # set attribute color
        self.curswin.bkgd('\0', wcolor|wflags)
        # draw elements
        for element in self.elements:
            self.curline += element.draw(self)
        # refresh the window
        self.curswin.refresh()
        # refresh all sub-windows created by sub-elements:
        for element in self.elements:
            element.refresh()
        # wait for input
        self.curswin.getkey()

    # get sub-element
    def getElementByName(self, name):
        for el in self.elements:
            if (el.name == name):
                return el
        return None

    # set field's value
    def setField(self, name, text):
        #for field in self.fields:
        #    if field.name == name:
        #        field.text = text
        None

    # get field's value
    def getField(self, name):
        #for field in self.fields:
        #    if field.name == name:
        #        return field.text
        #return None
        None

    # hide window
    def hide(self):
        self.hideFlag = True

