#!/usr/bin/python
import os
import argparse
import struct
from cStringIO import StringIO


def rtfDoc(r):
	from pyth.plugins.rtf15.reader import Rtf15Reader
	return Rtf15Reader.read(StringIO(r))

def rtfTextTerm(text, props):
	from termcolor import colored
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
	outParas = []
	for para in rtfDoc(r).content:
		outTexts = []
		for text in para.content:
			joined = ''.join(text.content)
			outTexts.append(rtfTextTerm(joined, text.properties))
		outParas.append(''.join(outTexts))
	return "\n".join(outParas)

def rtfHeader(r):
	p = rtfDoc(r).content[0]
	return ''.join([''.join(t.content) for t in p.content])

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

def printRtfs(rtfs):
	out = [rtfTerm(r) for r in rtfs]
	print "\n\n\n\n".join(out)

def writeRtfs(rtfs, outDir):
	if not os.path.exists(outDir):
		os.makedirs(outDir)
	
	names = []
	for r in rtfs:
		# Find a unique name
		header = rtfHeader(r).replace(os.sep, '_')[0:100]
		print header
		base = header
		suf = 0
		while base in names:
			suf += 1
			base = "%s %d" % (header, suf)
		names.append(base)
		name = "%s.rtf" % (base)
		
		with open(os.path.join(outDir, name), 'w') as f:
			f.write(r)

def parseStickies(dbPath):
	contents = file(dbPath).read()
	return findRtf(contents)	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Read OS X Stickies database")
	parser.add_argument('stickies', help="stickies database to parse")
	parser.add_argument('-r', '--rtf', dest='rtfOut', help="directory for RTF output")
	args = parser.parse_args()
	
	rtfs = parseStickies(args.stickies)
	if args.rtfOut:
		writeRtfs(rtfs, args.rtfOut)
	else:
		printRtfs(rtfs)
