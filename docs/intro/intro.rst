Introduction to XMLCurses Library
=================================

The purpose of this library is to make it easy to create
terminal-based interactive content using python and curses.
The basic idea of xmlcurses library is to let the programmer
describe the layout of the user interface using XML files,
then invoke the simple xmlcurses' module methods from the
python code in order to parse the XML descriptions,
populate the windows, and show them to the end-user.

UI Design Flow Using XMLCurses
------------------------------

A typical use case for xmlcurses is to create a terminal
window that accepts some kind of input, and processes
this input when a button is pressed. Finally, an output
might appear to the user indicating the results. A typical
design flow - for this general use case - shall be as follows:

1. Create XML File.
2. Describe terminal colors in XML.
3. Describe the window layout in XML, with named input/output
   elements and buttons.
4. In python, call XMLCurses initialization and XML parsing
   routines.
5. Use xmlcurses.getWindowByName() routine to get the
   window object.
6. Use xmlcurses.Window.getElementByName() routine
   to fetch input/output elements and buttons.
7. Initialize input elements with initial content,
   if they are not initialized with XML.
8. Set button event functions using 
   xmlcurses.ButtonBox.setAction(). The action function
   will be executed whenever the end user presses the key
   associated with that button in terminal. The action
   function usually processes the data, shows the
   result on output elements fetched in step 6,
   or hides the window.
9. Show the window using xmlcurses.Window.show(). This
   draws the window content on terminal and waits
   for input from user. The routine doesn't return
   unless xmlcurses.Window.hide() is called. It can
   be called by an action function as described in 8.

Using xmlcurses, you can easily create multiple windows and
switch between them on the terminal. The examples and tutorials
provided on this documentation will give you more insight and
show you good design practices using xmlcurses.

XML Layout
----------

The general layout for the XML file looks like this::

    <xml>
        <colors>
            --- color description goes here
        </colors>
        <windows>
            --- windows layout goes here
        </windows>
    </xml>

Inside the <colors> tag, the programmer defines color pairs 
as follows::

    <colors>
        <color name="pairname1" foreground="colorname" background="colorname" />
        <color name="pairname2" foreground="colorname" background="colorname" />
        <color name="pairname3" foreground="colorname" background="colorname" />
        etc.
    </colors>

That way, the programmer can define general color pairs that will be
initialized while parsing the XML file. The 'name' attribute is used
to setup a unique name that can be referenced later in the layout.
For example, if a window has its color attribute set to "pairname1", the text
in that window will have the corresponding foreground and background colors.

Currently supported colors are: white, red, yellow, green, blue, cyan,
magenta, and black.

Similarly, the user defines the layout for various windows inside the
windows tag::

    <windows>
        <window name="win1" width="val/percent" height="val/percent" color="pairname">
            --- window elements
        </window> 
        <window name="win2" width="val/percent" height="val/percent" color="pairname">
            --- window elements
        </window> 
        <window name="win3" width="val/percent" height="val/percent" color="pairname">
            --- window elements
        </window> 
        etc.
    </windows>

The 'name' attribute for a window (or an element) defines a unique name that can be
used by the programmer to reference the window or the element in code. Width
and height values can be either a raw integer number that describes how
much rows/columns the window spans (including window borders) or simply
a percentage of terminal size. Finally, the 'color' attribute refers to the color pair
used to fill the foreground and background colors for the text in the window.

Examples for window elements:

* **Title:**

    This element is used to create a title bar inside the window::

        <title name="elemname" text="Window Title" color="pairname" />

    The 'text' attribute defines the title for the window, and 'color'
    refers to the color pair used. The title is centered by default, and
    spans the whole width of the window. The height of the title is
    only one row.

* **Caption:**

    This is used to insert raw text inside the window::

        <caption name="elemname" text="Some text" align="left" color="pairname" />

    The attributes of <caption> is very similar to <title>, with the
    introduction of 'align' attribute which aligns the text inside the
    window.

* **Table:**

    This is used to define a table (with columns)::

        <table name="elemname" cols="A,B,C,D" height="val/percent" color="pairname" />

    The 'cols' attribute defines a list of column names that will be shown
    in the header of the table (separated by comma). The 'height' attribute
    can be an integer (number of rows) or a percentage of the empty space
    in the window. 

    For example, if the window height is 22 rows, the total
    of all other elements with predefined height is 10 rows, and the
    value of height is "70%", then the table will span 7 rows. A scroll
    bar is shown if the table has more rows than its display capacity.
    Please note that window borders span two rows of the window height.

* **Field:**

    Used to define a text-box for input::

        <field name="elemname" title="Data:" text="Initial" width="val/percent" color="pairname" />

    The 'title' of the field defines some text that will appear to the left of the
    text box; it works as a title for that field. The color for that title
    inherits the some color used for the parent window.  On the other hand,
    the 'text' attribute defines the initial value for the text box.
    
    The 'width' attribute is the total width for the field (both the title and 
    the text box). It can be either a percentage of window width or a raw number 
    of columns that the field spans. The field is centered by default.

* **ButtonBox:**

    A button box is a bar that appears at the bottom of the window. It
    contains several buttons like "OK", "CANCEL", "QUIT", and so on.
    The 'buttonbox' and 'button' tags is used to define that bar::

        <buttonbox name="elemname" color="pairname">
            <button key="key1" text=" BUTTON1 " />
            <button key="key2" text=" BUTTON2 " />
            <button key="key3" text=" BUTTON3 " />
        </buttonbox>

    This example buttonbox contains three buttons associated with
    three keys. The buttons will appear to the user arranged
    together in one bar::
    
        key1:[ BUTTON1 ] key2:[ BUTTON2 ] key3:[ BUTTON3 ] 

    The color pair used for 'key1:', 'key2:', and 'key3:' is the same
    color pair defined bythe 'color' attribute for the parent
    window. However, the color pair used for '[ BUTTON1 ]', 
    '[ BUTTON2 ]', and '[ BUTTON3 ]' is the color pair defined
    by the 'color' attribute of the buttton box. The end user
    will simply understand that they need to press key1 if
    they want to execute the functionality associated with button1,
    and so on.

    The 'key' attribute can be any keyboard key (such as "A", "B", etc.).
    It can also be a return key "RET", or the escape key "ESC". The
    button bar can be programmatically referenced in the python
    code using its name. xmlcurses.ButtonBox object supports
    methods that let a python method be executed whenever
    a specific key is pressed by the end user.

Python Code
-----------

As you can see, XML makes it very easy to describe the layout
of the user interface instead of doing that using python code.
Using the 'curses' library routines directly without an abstraction
layer results in a very complicated code. Our library makes
it easy to define standard curses window layouts/elements 
using XML and reference them in code.

In python, you will need to import the library first::

    import xmlcurses

Always keep the UI design flow described above in mind. First,
the python program should call xmlcurses' initialization routine::

    # initialize xmlcurses    
    xmlcurses.init()

Next step is to parse the XML file(s)::

    # parse the xml file
    xmlcurses.parse("<xml-file-name>")

Now the window layouts are loaded in memory. We can refer
to a window simply by its name to get its object::

    # get window instance
    win = xmlcurses.getWinByName("win1")

Now you can get the window elements using the 'name' attribute::

    # get window elements    
    fld = win.getElementByName("fieldelem")
    tbl = win.getElementByName("tableelem")
    box = win.getElementByName("butboxelem")

As easy as Javascript, right? Now you can manipulate window
elements in whatever way you like. For example, you can
initialize the fld element with some text::

    # initialize the textbox
    fld.setText("initial text")

You can add rows to the table::

    # add some row
    tbl.addRow({"A": 1, "B": 2, "C": 3, "D": 4})

Or set an action for the button box element::

    # add some action
    box.setAction("RET", lambda: win.hide())

Now we are ready to display the window::

    # show the window on terminal
    win.show()

The show() routine will return when win.hide() is executed.

What's Next
-----------

Start by installing xmlcurses library on your machine. Use
:doc:`../install/install` manual page to
guide you on the installation procedure.

Next, I suggest you check the examples under examples/ directory in the
source code (they are explained in the documentation page:
:doc:`../examples/examples`) for typical use cases. If you are
too stupid and the examples are not clear enough to you
because you have mental health issues, check the tutorial page:
:doc:`../tutorial/tutorial`.

Now you are ready to start coding with xmlcurses by yourself.
While you are coding, refer to :doc:`../xml/xml` and 
:doc:`../classes/classes` manual pages
for the listing of all XML tags/attributes and
python classes/objects/methods/attributes of the library,
respectively.

