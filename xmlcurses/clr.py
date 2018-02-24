#!/usr/bin/env python

class Color:
    con        = None
    name       = ""
    foreground = ""
    background = ""
    pairid     = 1
    lastpairid = 1

    def __init__(self):
        self.pairid      = Color.lastpairid
        Color.lastpairid = Color.lastpairid + 1

