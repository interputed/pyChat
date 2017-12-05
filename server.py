#!/usr/bin/python3

# Andrew Craighead
# December 4th, 2017
# Lab 3 Server


import socket, sys, json

print("My chat room server. Version One.")

# Setting up connection socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 13707))
# Only need to listen for one connection
sock.listen(1)
connection, address = sock.accept()

# Login status variables
loggedin = False
userid = ""


# Opens JSON file containing user login info
# Note: I do not condone storing login passwords as plain text
with open('userdata.json') as ufile:
	userdata = json.load(ufile)


# Functions for chat commands
# Logs in a user if it exists
def login(msg):
	global userid, loggedin
	words = msg.split(" ")
	username = words[1]
	password = words[2]

	for u in userdata['users']:
		if u['uname'] == username:
			if u['pw'] == password:
				loggedin = True
				userid = username
				print(username + " login.")
				return ">Server: " + username + " joins"
			
			break

	return ">Server: Denied. Invalid login."


# Sends a message to the chat or rejects if not logged in
def send(msg):
	if loggedin == True:
		message = msg[5:]
		print(userid + ": " + message) 
		return ">" + userid + ": " + message

	else:
		return ">Server: Denied. Please login first."


# Logout user
def logout():
	global userid, loggedin
	if loggedin == False:
		return ">Server: Already logged out"
	else:
		string = ">Server: " + userid + " left."
		print(userid + " logout.")
		userid = ""
		loggedin = False
		return string


# Creates new user if it doesn't exist
def newuser(msg):
	global userid, loggedin, userdata

	if loggedin == True:
		return ">Server: Denied. User already logged in, please logout first."
	
	else:
		words = msg.split(" ")
		username = words[1]
		password = words[2]

		if len(username) >= 32 or len(username) <= 1:
			return ">Server: Denied. Username must be between 2 and 31 characters in length."

		elif len(password) > 8 or len(password) < 4:
			return ">Server: Denied. Password must be between 4 and 8 characters in length."

		else:
			for u in userdata['users']:
				if u['uname'] == username:
					return ">Server: Denied. Username already exists."

		new_entry = dict(uname = username, pw = password)

		userdata['users'].append(new_entry)

		with open('userdata.json', 'w') as f:
			json.dump(userdata, f)

		userid = username
		loggedin = True

		return ">Server: " + username + " joins"



# No switch-case statement in Python? Wtf?
def switcher(cmd, msg):
	if cmd == "login":
		return login(msg)

	elif cmd == "newuser":
		return newuser(msg)

	elif cmd == "send":
		return send(msg)

	elif cmd == "logout":
		return logout()

	else:
		# print("ERROR: Invalid command")
		return "ERROR"


# Infinite Loop FTW
while True:
	# Should be no need for a message longer than 256 bytes
	recv_msg = connection.recv(256).decode()

	# Gets the first word only of the message
	cmd = recv_msg.split(" ")[0]

	# commands are not case sensitive
	send_msg = switcher(cmd.lower(), recv_msg)

	if send_msg == "ERROR":
		break

	connection.send(send_msg.encode())


connection.close()
print("Connection closed")