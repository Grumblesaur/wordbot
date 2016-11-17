def ping(msg, conn):
	if msg.find("PING") > -1:
		conn.send("PONG %s\r\n" % msg.split()[1])
		return "PING"
	return ""

def sanitize(msg):
	msg = msg.lower()
	for char in msg:
		if char in '?.!/;:,()[]{}#$%^&*@!"':
			msg = msg.replace(char,'')
	print msg
	return msg

def is_ascii(string):
	try:
		string.decode('ascii')
	except UnicodeDecodeError as ude:
		print ude
		return False
	else:
		return True

def collect(data, main, user):
	for word in data:
		try:
			main[word] += 1
		except KeyError as ke:
			print ke
			if word not in user:
				user[word] = 1
			else:
				user[word] += 1

def join_channel(msg, conn, chan, flag):
	conn.send("JOIN %s\r\n" % chan)
	if '@' in msg and not flag:
		print "join"
		return True
	return False

def cleanup(main, user):
	now = datetime.datetime.now()
	with open("out/" + str(now).split()[1] + ".txt", 'w') as out:
		for word, count in main.items():
			out.write("%s, %s\n" % (word, count))
		for word, count in user.items():
			out.write("%s, %s\n" % (word, count))
	out.close()

def handle(signum, frame):
	print("Process killed.")
	cleanup(words, user_words)
	sys.exit(0)

