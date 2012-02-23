#pystickies
---

Converts the database from the Mac's "Stickies" program into RTF files, one per sticky. This is platform-independent, it doesn't use Cocoa to do the conversion, but rather uses heuristics to find the RTF data.

##Requirements

[pyth](https://github.com/brendonh/pyth)
[termcolor](http://pypi.python.org/pypi/termcolor) (optional, for printing to the terminal)

##Examples

###Print your stickies to the terminal

	./pystickies.py ~/Library/StickiesDatabase

###Output RTF files to a directory

	 ./pystickies.py --rtf ~/path/to/dir ~/Library/StickiesDatabase

#htmlsync
---

One-directionally syncs the Stickies database to a directory of HTML files. Only works on OS X, thanks to the lovely 'textutil' text conversion tool.

#launchdgen
---

A launchd agent that watches the Stickies database for changes, and keeps it always in sync with a directory of HTML files.

###Put your Stickies on Dropbox

	./launchdgen.py --launchAgent ~/Dropbox/Stickies
