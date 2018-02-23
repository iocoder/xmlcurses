#!/usr/bin/env python

from curses.textpad import Textbox, rectangle

# add spaces to string to align it to the center
def center(string, width):
    padleft  = "".join(([" "] * ((width - len(string))/2)))
    padright = "".join(([" "] * (width - len(string) - len(padleft))))
    return padleft + string + padright

# validate keyboard input for textbox
def validate(ch):
    global edit_cmd
    if ch == 10:
        # enter
        edit_cmd = ch
        ch = 7
    if ch == 27:
        # escape
        edit_cmd = ch
        ch = 7
    elif ch == 259:
        # key up
        edit_cmd = ch
        ch = 7
    elif ch == 258:
        # key down
        edit_cmd = ch
        ch = 7
    return ch

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
    curswin   = None    # pointer to curses' window structure
    firstline = 1       # first line for window content
    edit_cmd  = 0       # used for textbox manipulation

    # print title line
    def printTitle(self):
        # get global pointers
        curses  = self.curses
        actions = self.actions
        # get curses' window structure
        curswin = self.curswin
        # get window size
        rows, cols = curswin.getmaxyx()
        # get first line for window content
        firstline = self.firstline
        # check whether the title string is not empty
        if (self.title != ""):
            # print the title
            curswin.addstr(firstline, 1, center(self.title, cols-2), 
                           curses.color_pair(1)|curses.A_BOLD)
            # update firstline
            self.firstline += 2

    # print caption
    def printCaption(self):
        # get global pointers
        curses  = self.curses
        actions = self.actions
        # get curses' window structure
        curswin = self.curswin
        # get window size
        rows, cols = curswin.getmaxyx()
        # get first line
        firstline = self.firstline
        # check whether captext is empty or not
        if (self.captext != ""):
            if (self.capalign == "center"):
                curswin.addstr(firstline, 1, center(self.captext, cols-2), 
                               curses.color_pair(2)|curses.A_BOLD);
            elif (self.capalign == "left"):
                curswin.addstr(firstline, 2, self.captext, 
                               curses.color_pair(2)|curses.A_BOLD);
            # update firstline       
            self.firstline += 2

    # print buttons line
    def printButtons(self):
        # get global pointers
        curses  = self.curses
        actions = self.actions
        # get curses' window structure
        curswin = self.curswin
        # get width and height
        max_y, max_x = curswin.getmaxyx()
        line = max_y - 2
        cols = max_x - 2
        # move cursor to line
        curswin.move(line, 1)
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

    # print table contents
    def printTable(self):
        # get global pointers
        curses  = self.curses
        actions = self.actions
        # get curses' window structure
        curswin = self.curswin
        # get first line
        firstline = self.firstline
        # get window width
        rows, cols = curswin.getmaxyx()
        # initialize current selected row
        if (len(self.tbldata) > 0):
            self.selrow = 0
        else:
            self.selrow = -1
        # dashes
        dashes  = "".join(["-" * (cols-2)])
        curswin.addstr(firstline+0, 1, dashes, curses.color_pair(2)|curses.A_BOLD)
        # print table titles
        colwidth = (cols-3)/len(self.tblcols)
        curswin.move(firstline+1, 1)
        for tblcol in self.tblcols:
            curswin.addstr(center(tblcol, colwidth), 
                           curses.color_pair(2)|curses.A_BOLD)
        # dashes again
        curswin.addstr(firstline+2, 1, dashes, curses.color_pair(2)|curses.A_BOLD)
        last_line   = rows - 4
        # print table rows
        while not self.hideFlag:
            # print rows
            cur_row = 0
            for row in self.tbldata:
                # move to row line
                curswin.move(firstline+cur_row+3, 1)
                # initialize color
                if (cur_row == self.selrow):
                    # selected row
                    color = curses.color_pair(3)|curses.A_BOLD|curses.A_REVERSE
                else:
                    # normal color for other rows
                    color = curses.color_pair(3)|curses.A_BOLD 
                # loop over columns
                for col in self.tblcols:
                    # get cell value
                    cell = row[col]
                    # add cell
                    curswin.addstr(center(cell, colwidth), color)
                # print some padding spaces
                while True:
                    y, x = curswin.getyx()
                    if (x < cols-1):
                        curswin.addstr(" ", color)
                    else:
                        break
                # have finshed one row
                cur_row = cur_row + 1
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
    def printFields(self):
        # get global pointers
        curses  = self.curses
        actions = self.actions
        # get curses' window structure
        curswin = self.curswin
        # get first line
        firstline = self.firstline
        # get window width
        rows, cols = curswin.getmaxyx()
        # calculate field's title width
        titlewidth = max(len(fld.title) for fld in self.fields)+1
        # print fields
        cur_field = 0
        txtwins  = []
        txtboxes = []
        for field in self.fields:
            # calculate textbox width
            totwidth  = cols-4-titlewidth
            textwidth = 0
            if (field.width[-1] == "%"):
                textwidth = int(field.width[:-1])*(totwidth)/100
            else:
                textwidth = min(int(field.width), totwidth)
            x = (cols-4-textwidth-titlewidth)/2+2
            # move to line
            curswin.move(firstline+cur_field, x)
            # print title
            curswin.addstr(field.title)
            # text window
            txtwin = curses.newwin(1, textwidth, firstline+cur_field, x+titlewidth)
            txtwin.bkgd('\0', curses.color_pair(4))
            txtwin.clear()
            txtwins.append(txtwin)
            # if edit, insert val
            txtwin.addstr(field.text)
            # create an editable box over the window
            txtbox = Textbox(txtwin)
            txtboxes.append(txtbox)        
            # next field
            cur_field = cur_field + 1
        # refresh display
        curswin.refresh()
        for txtwin in txtwins:
            txtwin.refresh()
        # show cursor    
        curses.curs_set(1)
        cur_box = 0
        # edit the boxes
        while not self.hideFlag:
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
        curswin.border()
        self.curswin = curswin        
        cur_line = 0
        # title
        self.printTitle()
        # caption
        self.printCaption()
        # print buttons
        self.printButtons()
        # print window contents
        if (self.style == "table"):
            # print table elements and wait for actions
            self.printTable()
        elif (self.style == "input"):
            # print fields and wait for actions
            self.printFields()


    # add row to table
    def addRow(self, row):
        self.tbldata.append(row)

    # set field's value
    def setField(self, name, text):
        for field in self.fields:
            if field.name == name:
                field.text = text

    # get field's value
    def getField(self, name):
        for field in self.fields:
            if field.name == name:
                return field.text
        return None

    # hide window
    def hide(self):
        self.hideFlag = True

