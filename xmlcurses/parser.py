#!/usr/bin/env python

import xml.etree.ElementTree as ET

from err    import XMLException
from win    import Window
from btn    import Button
from fld    import Field

def parse(xmlfile, wins):
    # parse XML file
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    for xmlwin in root:
        # read window parameters
        if xmlwin.tag != 'window':
            raise XMLException("Highest-level of XML tags should be 'window'")
        win = Window()
        win.name   = xmlwin.attrib["name"]
        win.width  = xmlwin.attrib["width"]
        win.height = xmlwin.attrib["height"]
        win.style  = xmlwin.attrib["style"]
        if win.style not in ["table", "input", "message"]:
            raise XMLException("Invalid window style: " + win.style)
        # read sub-elements of the window
        for xmlelm in xmlwin:
            if xmlelm.tag == "title":
                # title
                win.title   = xmlelm.attrib["text"]
            elif xmlelm.tag == "caption":
                # caption
                win.captext = xmlelm.attrib["text"]
                win.capalign = xmlelm.attrib["align"]
                if win.capalign not in ["left", "right", "center"]:
                    raise XMLException("Invalid value for align: " + win.capalign)
            elif xmlelm.tag == "table":
                # table
                win.tblcols = xmlelm.attrib["cols"].split(',')
            elif xmlelm.tag == "field":
                # field
                fld = Field()
                fld.name  = xmlelm.attrib["name"]
                fld.title = xmlelm.attrib["title"]
                fld.text  = xmlelm.attrib["text"]
                win.fields.append(fld)
            elif xmlelm.tag == "button":
                # button
                btn = Button()
                btn.text   = xmlelm.attrib["text"]
                btn.key    = xmlelm.attrib["key"]
                btn.action = xmlelm.attrib["action"]
                btn.win    = win
                win.buttons.append(btn)
            else:
                raise XMLException("Invalid XML tag: " + xmlelm.tag)
        # add window
        wins[win.name] = win

