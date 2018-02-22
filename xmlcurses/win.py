#!/usr/bin/env python

def center(string, width):
    padleft  = "".join(([" "] * ((width - len(string))/2)))
    padright = "".join(([" "] * (width - len(string) - len(padleft))))
    return padleft + string + padright

class Window:
    name      = ""      # window XML identifier
    width     = ""      # window XML width
    height    = ""      # window XML height
    style     = ""      # window XML style
    title     = ""      # XML <title> tag, text
    captext   = ""      # XML <caption> tag, text
    capalign  = ""      # XML <caption> tag, align
    selrow    = -1      # current selected row in a table
    tblcols   = []      # XML table column names
    tbldata   = []      # content of the data in the table
    fields    = []      # XML table fields
    buttons   = []      # XML table buttons
    hideFlag  = False   # To be hidden after action execution
    curses    = None    # pointer to curses module
    actions   = None    # pointer to action list

    # print buttons line
    def printButtons(self, curswin):
        # get global pointers
        curses  = self.curses
        actions = self.actions
        # store old y and x
        old_y, old_x = curswin.getyx()
        # get width and height
        max_y, max_x = curswin.getmaxyx()
        line = max_y - 2
        cols = max_x
        # move cursor to line
        curswin.move(line, 0)
        # padding
        btnswidth = 0
        for btn in self.buttons:
            btnswidth += len(btn.key) + len(btn.text) + 2
        spaces  = "".join([" " * ((cols-btnswidth)/2)])
        curswin.addstr(spaces)
        # print buttons
        for btn in self.buttons:
            curswin.addstr(btn.key)
            curswin.addstr(":")
            curswin.addstr(btn.text, curses.color_pair(1)|curses.A_BOLD)
            curswin.addstr("  ")
        # return to old y and x coordinates
        curswin.move(old_y, old_x)

    def printTable(self, curswin, first_line):
        # get global pointers
        curses  = self.curses
        actions = self.actions
        # initialize current selected row
        if (len(self.tbldata) > 0):
            self.selrow = 0
        else:
            self.selrow = -1
        # get window width
        rows, cols = curswin.getmaxyx()
        # move to window contents
        curswin.move(first_line, 0)
        # dashes
        dashes  = "".join(["-" * cols])
        curswin.addstr(dashes, curses.color_pair(2)|curses.A_BOLD)
        # print table titles
        colwidth = (cols-1)/len(self.tblcols)
        for tblcol in self.tblcols:
            curswin.addstr(center(tblcol, colwidth), 
                           curses.color_pair(2)|curses.A_BOLD)
        curswin.addstr("\n")
        # dashes again
        curswin.addstr(dashes, curses.color_pair(2)|curses.A_BOLD)
        # calculate table borders
        first_line += 3
        last_line   = rows - 4
        # print table row
        while not self.hideFlag:
            # move to table head
            curswin.move(first_line, 0)
            # print rows
            cur_row = 0
            max_row = 0
            for row in self.tbldata:
                for col in self.tblcols:
                    # get cell value
                    cell = row[col]
                    if (cur_row == self.selrow):
                        # selected row
                        color = curses.color_pair(3)|curses.A_BOLD|curses.A_REVERSE
                    else:
                        # normal color for other rows
                        color = curses.color_pair(3)|curses.A_BOLD 
                    # add cell
                    curswin.addstr(center(cell, colwidth), color)
                # add linefeed
                cur_row = cur_row + 1
                max_row = max_row + 1
                curswin.addstr("\n")
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
    def printFields(self, curswin, first_line):
        None

    def show(self):
        # get global pointers
        curses  = self.curses
        actions = self.actions
        # clear hide attribute
        self.hideFlag = False
        # get elements from curses module
        totlines = curses.LINES
        totcols  = curses.COLS
        # initialize dimensions
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
        curswin = curses.newwin(rows, cols, winy, winx)
        cur_line = 0
        # title
        if (self.title != ""):
            curswin.addstr(center(self.title, cols), 
                           curses.color_pair(1)|curses.A_BOLD)
            cur_line += 1
        # empty line
        curswin.addstr("\n")
        cur_line += 1 
        # caption
        if (self.captext != ""):
            if (self.capalign == "center"):
                curswin.addstr(center(self.captext, cols), 
                               curses.color_pair(2)|curses.A_BOLD);
                cur_line += 1
            elif (self.capalign == "left"):
                curswin.addstr(self.captext + "\n", 
                               curses.color_pair(2)|curses.A_BOLD);
                cur_line += 1
            # empty line after caption            
            curswin.addstr("\n")
            cur_line += 1
        # calculate first_line for window content
        first_line = cur_line
        # print buttons
        self.printButtons(curswin)
        # print window contents
        if (self.style == "table"):
            # print table elements and wait for actions
            self.printTable(curswin, first_line)

    # add row to table
    def addRow(self, row):
        self.tbldata.append(row)

    # set field's value
    def setField(self, name, text):
        for field in self.fields:
            if field.name == name:
                field.text = val

    # get field's value
    def getField(self, name):
        for field in self.fields:
            if field.name == name:
                return field.text
        return None

    # hide window
    def hide(self):
        self.hideFlag = True

