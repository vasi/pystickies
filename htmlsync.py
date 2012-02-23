#!/usr/bin/python
import os
import sys
import argparse
import subprocess
import tempfile

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Sync OS X Stickies with HTML files")
	parser.add_argument('stickies', help="stickies database to parse")
	parser.add_argument('outDir', help="directory for HTML files")
	parser.add_argument('-c', '--cache', dest='cache', help="directory for intermediaries")
	args = parser.parse_args()
	
	# Clean up cache
	cacheDir = args.cache or tempfile.mkdtemp()
	if not os.path.exists(cacheDir):
		os.makedirs(cacheDir)
	for f in os.listdir(cacheDir):
		os.remove(os.path.join(cacheDir, f))
	
	# Run pystickies
	pystickies = os.path.join(os.path.dirname(__file__), 'pystickies.py')
	subprocess.check_call([pystickies, '--rtf', cacheDir, args.stickies])
	
	# Sync it up
	if not os.path.exists(args.outDir):
		os.makedirs(args.outDir)
	unwanted = set(os.listdir(args.outDir))
	
	for srcName in os.listdir(cacheDir):
		name, ext = os.path.splitext(srcName)
		if ext != ".rtf":
			continue
		dstName = name + ".html"
		
		src = os.path.join(cacheDir, srcName)
		dst = os.path.join(args.outDir, dstName)
		# textutil only exists on OS X!
		subprocess.check_call(['textutil', '-convert', 'html', '-output', dst, src])
		unwanted.discard(dstName)
	for f in unwanted:
		os.remove(os.path.join(args.outDir, f))
