#!/usr/bin/env python

class Context:
    # sharable context between all xmlcurses modules
    curses  = None
    wins    = None
    colors  = None
    # error printing
    olderr  = None
    newerr  = None

