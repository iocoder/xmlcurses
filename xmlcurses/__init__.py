#!/usr/bin/env python

import curses
import atexit

from win    import Window
from parser import parse

stdscr  = None
wins    = {}
actions = {}

def init(xmlfile):
    global stdscr
    # create window structures
    parse(xmlfile, wins)
    # initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    # clear screen
    stdscr.clear()
    # hide cursor
    curses.curs_set(0)
    # initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE,  curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN,  curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK,  curses.COLOR_YELLOW)

def addAction(name, func):
    actions[name] = func

def term():
    # reset terminal settings
    curses.endwin()

def newWinByName(name):
    win = Window()
    win.__dict__ = wins[name].__dict__.copy()
    win.curses  = curses
    win.actions = actions
    return win

