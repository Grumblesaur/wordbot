#!/usr/bin/python

import socket
import sys
import datetime
import signal
from bot_help import *

words = {}; user_words = {}


signal.signal(signal.SIGTERM, handle)

# constants
nick = "wordbot"
serv = "irc.gamesurge.net"
port = 6667
chan = "#limittheory"

# alias the console-out function to a shorter name
log = sys.stdout.write

## procedure start ##

# populate dictionary with words to track
with open("/usr/share/dict/words") as amer_engl:
	for line in amer_engl:
		if is_ascii(line):
			words[line.lower().strip()] = 0

# connect to IRC server
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((serv, port))
irc.recv(4096)
irc.send("NICK %s\r\n" % nick)
irc.send("USER %s %s %s :Grumblesaur IRC\r\n" % (nick, nick, nick))
irc.send("JOIN %s\r\n" % chan)
print "connect"

given_voice = False
scanning = ignore = True
while scanning:
	try:
		# ping when requested
		data = irc.recv(1024)
		if ping(data, irc):
			print "ping"
			continue # don't add pings to the dictionary
		# join channel
		if not given_voice:
			given_voice = join_channel(data, irc, chan, given_voice)
		# wait for the IRC boilerplate to finish being sent to wordbot
		if ignore:
			if "mode %s +v %s" % (channel[1:],nick) in data:
				ignore = False
			continue
		# collect word usage data
		data = sanitize(data.strip()).split()[3:]
		collect(data, words, user_words)
	except KeyboardInterrupt as e:
		scanning = False

cleanup(words, user_words)

