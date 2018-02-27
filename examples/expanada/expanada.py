#!/usr/bin/env python2

# xmlcurses library
import xmlcurses

# local window classes
from WinLogin        import WinLogin
from WinPeriods      import WinPeriods
from WinAddPeriod    import WinAddPeriod
from WinEditPeriod   import WinEditPeriod
from WinTransacts    import WinTransacts
from WinAddTransact  import WinAddTransact
from WinEditTransact import WinEditTransact

# MySQL helper
from Session  import Session

# context
con = {}

# initialize xmlcurses    
xmlcurses.init()

# parse colors
xmlcurses.parse("Colors.xml")

# save this instance of xmlcurses in the context variable
con["xmlcurses"] = xmlcurses

# create a SQL session
con["session"] = Session()

# create window structures and save in contexts
con["winLogin"       ] = WinLogin       (con)
con["winPeriods"     ] = WinPeriods     (con)
con["winAddPeriod"   ] = WinAddPeriod   (con)
con["winEditPeriod"  ] = WinEditPeriod  (con)
con["winTransacts"   ] = WinTransacts   (con)
con["winAddTransact" ] = WinAddTransact (con)
con["winEditTransact"] = WinEditTransact(con)

# show winLogin
con["winLogin"].show()

