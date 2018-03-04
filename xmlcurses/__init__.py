#!/usr/bin/env python

# external libraries and modules
import curses
import curses.textpad
import xml.etree.ElementTree
import atexit
import os
import tempfile
import sys

# xmlcurses library context
from .con import Context

# submodules public to the user of xmlcurses
from .clr import Color
from .win import Window
from .ttl import Title
from .cap import Caption
from .tbl import Table
from .fld import Field
from .box import ButtonBox

# errors
from .err import XMLException

#################################################################
#                      Context Manipulation                     #
#################################################################

# create a new context for xmlcurses library
con = Context()
con.curses    = curses
con.wins      = {}
con.colors    = {}
con.tmpdir    = ""
con.errfile   = ""
con.stderr    = None
# initialize all submodules with this context
Color.con     = con
Window.con    = con
Title.con     = con
Caption.con   = con
Table.con     = con
Field.con     = con
ButtonBox.con = con

#################################################################
#                         XML Parsing                           #
#################################################################

def parseColors(xmltree):
    # parse xml
    for xmlcolor in xmltree:
        # check the validity of the XML tag
        if xmlcolor.tag != 'color':
            raise XMLException("Expected 'color' tag, found: " + xmlcolor.tag)
        # read color parameters
        color = Color()
        color.name       = xmlcolor.attrib["name"]
        color.foreground = xmlcolor.attrib["foreground"]
        color.background = xmlcolor.attrib["background"]
        # add the color
        addColor(color)

def parseWindows(xmltree):
    # parse xml
    for xmlwin in xmltree:
        # check the validity of the XML tag
        if xmlwin.tag != 'window':
            raise XMLException("Expected 'window' tag, found: " + xmlwin.tag)
        # read window parameters
        win = Window()
        win.name   = xmlwin.attrib["name"]
        win.width  = xmlwin.attrib["width"]
        win.height = xmlwin.attrib["height"]
        win.color  = xmlwin.attrib["color"]
        # read sub-elements of the window
        for xmlelm in xmlwin:
            if xmlelm.tag == "title":
                # title
                title         = Title()
                title.name    = xmlelm.attrib["name"]
                title.text    = xmlelm.attrib["text"]
                title.color   = xmlelm.attrib["color"]
                win.addElement(title)
            elif xmlelm.tag == "caption":
                # caption
                caption       = Caption()
                caption.name  = xmlelm.attrib["name"]
                caption.text  = xmlelm.attrib["text"]
                caption.align = xmlelm.attrib["align"]
                caption.color = xmlelm.attrib["color"]
                win.addElement(caption)
            elif xmlelm.tag == "table":
                # table
                table          = Table()
                table.name     = xmlelm.attrib["name"]
                table.colnames = xmlelm.attrib["cols"].split(',')
                table.height   = xmlelm.attrib["height"]
                table.color    = xmlelm.attrib["color"]
                win.addElement(table)
            elif xmlelm.tag == "field":
                # field
                fld = Field()
                fld.name  = xmlelm.attrib["name"]
                fld.title = xmlelm.attrib["title"]
                fld.text  = xmlelm.attrib["text"]
                fld.width = xmlelm.attrib["width"]
                fld.color = xmlelm.attrib["color"]
                win.addElement(fld)
            elif xmlelm.tag == "buttonbox":
                # button box
                box = ButtonBox()
                box.name  = xmlelm.attrib["name"]
                box.color = xmlelm.attrib["color"]
                for xmlbtn in xmlelm:
                    if xmlbtn.tag == "button":
                        btn_key    = xmlbtn.attrib["key"]
                        btn_text   = xmlbtn.attrib["text"]
                        box.addButton(btn_key, btn_text)
                    else:
                        raise XMLException("Expected 'button' tag: " + btn.tag)
                win.addElement(box)
            else:
                raise XMLException("Invalid element tag: " + xmlelm.tag)
        # add window
        addWindow(win)

def parse(xmlfile):
    # parse XML file
    tree = xml.etree.ElementTree.parse(xmlfile)
    root = tree.getroot()
    for rootel in root:
        if rootel.tag == 'windows':
            # parse windows
            parseWindows(rootel)
        elif rootel.tag == 'colors':
            # parse colors
            parseColors(rootel)
            None
        else:
            # error
            raise XMLException("Expected 'windows' or 'colors' tag: " + rootel.tag)

#################################################################
#                    Instance Manipulation                      #
#################################################################

def addWindow(win):
    # add window to wins directory
    con.wins[win.name] = win

def addColor(color):
    # get context vars
    curses = con.curses
    wins   = con.wins
    colors = con.colors
    # add to colors
    colors[color.name] = color
    # color string to curses mapping
    cursesColors = {"white":   curses.COLOR_WHITE,
                    "red":     curses.COLOR_RED,
                    "yellow":  curses.COLOR_YELLOW,
                    "green":   curses.COLOR_GREEN,
                    "blue":    curses.COLOR_BLUE,
                    "cyan":    curses.COLOR_CYAN,
                    "magenta": curses.COLOR_MAGENTA,
                    "black":   curses.COLOR_BLACK}
    # get attributes
    pairid     = color.pairid
    foreground = cursesColors[color.foreground]
    background = cursesColors[color.background]
    # add to curses
    curses.init_pair(pairid, foreground, background)

def getWinByName(name):
    return con.wins[name]

#################################################################
#                     Library Destruction                       #
#################################################################

def init():
    # open a new pipe
    pipein, pipeout = os.pipe()
    # store current stderr and the pipe
    con.olderr  = os.dup(sys.stderr.fileno())
    con.newerr  = pipein
    # redirect stderr to the pipe
    os.dup2(pipeout, sys.stderr.fileno())
    # write something to the pipe
    sys.stderr.write("Initializing xmlcurses...\n")
    # initialize curses
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    # call close on exit
    atexit.register(close)

def close():
    # reset terminal settings
    curses.endwin()
    # write something to the pipe
    sys.stderr.write("Closing xmlcurses...\n")
    # redirect stderr to the old one
    os.close(sys.stderr.fileno())
    os.dup2(con.olderr, sys.stderr.fileno())
    # now read & print the messages stored inside the pipe!
    while True:  
        data = os.read(con.newerr, 100)
        sys.stderr.write(data.decode("ascii"))
        if len(data) < 100:
            break

