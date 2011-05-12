#!/usr/bin/python
import sys
import struct
from cStringIO import StringIO

from termcolor import colored
from pyth.plugins.rtf15.reader import Rtf15Reader

def rtfTextTerm(text, props):
	attrs = None
	if 'bold' in props:
		attrs = ['bold']
	elif 'underline' in props:
		attrs = ['underline']
	
	color = None
	if 'italic' in props:
		color = 'blue'
	
	return colored(text, color, attrs = attrs)

def rtfTerm(r):
	doc = Rtf15Reader.read(StringIO(r))
	outParas = []
	for para in doc.content:
		outTexts = []
		for text in para.content:
			joined = ''.join(text.content)
			outTexts.append(rtfTextTerm(joined, text.properties))
		outParas.append(''.join(outTexts))
	return "\n".join(outParas)

def findRtf(s):
	rtfs = []
	pos = 0
	needle = '{\\rtf1'
	while True:
		pos = s.find(needle, pos + 4)
		if pos == -1:
			return rtfs
		size = struct.unpack_from('<L', s, pos - 4)[0]
		rtfs.append(s[pos : pos + size])
		pos += size

def printStickies(path):
	contents = file(path).read()
	rtfs = findRtf(contents)
	out = [rtfTerm(r) for r in rtfs]
	print "\n\n\n\n".join(out)

if __name__ == '__main__':
	stickiesDB = sys.argv[1]
	printStickies(stickiesDB)
