import socket
import sys
import datetime

def ping(msg, conn):
	if msg.find("PING") > -1:
		conn.send("PONG %s\r\n" % data.split()[1])
		return "PING"
	return ""

def sanitize(msg):
	msg = msg.lower()
	for char in msg:
		if char in '?.!/;:,()[]{}#$%^&*@!"':
			msg = msg.replace(char,'')
	return msg

def is_ascii(string):
	try:
		string.decode('ascii')
	except UnicodeDecodeError:
		return False
	else:
		return True

def collect(data, main, user):
	for word in data:
		try:
			main[word] += 1
		except KeyError as ke:
			if word not in user:
				user[word] = 1
			else:
				user[word] += 1

# constants
nick = "wordbot"
serv = "irc.gamesurge.net"
port = 6667
chan = "#limittheory"

# alias the console-out function to a shorter name
log = sys.stdout.write

## procedure start ##

# populate dictionary with words to track
words = {}; user_words = {}
with open("/usr/share/dict/american-english") as amer_engl:
	for line in amer_engl:
		if (is_ascii(line)):
			words[line.lower()] = 0

# connect to IRC server
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((serv, port))
irc.recv(4096)
irc.send("NICK " + nick + "\r\n")
irc.send("USER " + nick + " " + nick + " " + nick + ":Grumblesaur IRC\r\n")
irc.send("JOIN " + chan + "\r\n")

connected = False
scanning = True
ignore = True
while scanning:
	try:
		# ping when requested
		data = irc.recv(1024)
		if ping(data, irc):
			print "ping"
			continue # don't add pings to the dictionary
		
		# ensure that we are in the channel
		if connected == False:
			irc.send("JOIN " + chan + "\r\n")
		if "@" in data and connected == False:
			connected = True
			print "connect"
		
		# wait for the IRC boilerplate to finish being sent to wordbot
		if ignore:
			if "mode limittheory +v wordbot" in data:
				ignore = False
			continue
		
		# collect word usage data
		data = sanitize(data)
		print data
		data = data.split()[3:]
		collect(data, words, user_words)

	except KeyboardInterrupt as e:
		scanning = False

now = datetime.datetime.now()

with open("out/" + str(now) + ".txt", 'w') as out:
	for word, count in words.items():
		out.write("%s, %s\n" % (word, count))
	for wn in user_words.items():
		out.write("%s, %s\n" % (word, count))
