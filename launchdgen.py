#!/usr/bin/python
import os
import string
import subprocess
import argparse

templ = string.Template("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>$name</string>
	<key>ProgramArguments</key>
	<array>
		<string>$progDir/htmlsync.py</string>
		<string>--cache</string>
		<string>$home/Library/Caches/stickiessync</string>
		<string>$db</string>
		<string>$outDir</string>
	</array>
	<key>WatchPaths</key>
	<array>
		<string>$db</string>
	</array>
	<key>ThrottleInterval</key>
	<integer>10</integer>
	<key>EnvironmentVariables</key>
	<dict>
		<key>PYTHONPATH</key>
		<string>$pylib</string>
	</dict>
</dict>
</plist>
""")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Generate launchd plist for syncing stickies")
	parser.add_argument('outDir', help="directory to sync to")
	parser.add_argument('-u', '--user', dest='user', help="user whose stickies to watch")
	parser.add_argument('-p', '--prog', dest='progDir', help="path to executables")
	parser.add_argument('-d', '--domain', dest='domain', help="reverse-domain identifier")
	parser.add_argument('--pylib', dest='pylib', help="value of PYTHONPATH")
	parser.add_argument('-l', '--launchAgent', dest='launchAgent', action='store_true',
		help="create plist in LaunchAgents dir")
	args = parser.parse_args()
	
	user = args.user or os.environ['USER']
	home = os.path.expanduser("~%s" % (user,))
	db = os.path.join(home, 'Library', 'StickiesDatabase')
	progDir = args.progDir or os.path.realpath(os.path.dirname(__file__))
	domain = args.domain or user
	name = domain + ".stickiessync"
	pylib = args.pylib or os.environ['PYTHONPATH']
	
	s = templ.substitute(user=user, home=home, db=db, progDir=progDir,
		name=name, pylib=pylib, outDir=os.path.realpath(args.outDir))
	
	fname = name + ".plist"
	if args.launchAgent:
		path = os.path.join(home, 'Library', 'LaunchAgents', fname)
		if os.path.exists(path):
			subprocess.check_call(['launchctl', 'unload', path])			
		f = open(os.path.join(home, 'Library', 'LaunchAgents', fname), 'w')
		f.write(s)
		f.close()
		subprocess.check_call(['launchctl', 'load', path])
	else:
		print s
