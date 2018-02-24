#!/usr/bin/env python

# add spaces to string to align it to the center
def center(string, width):
    padleft  = "".join(([" "] * ((width - len(string))/2)))
    padright = "".join(([" "] * (width - len(string) - len(padleft))))
    return padleft + string + padright

