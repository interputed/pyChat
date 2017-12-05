#!/usr/bin/python3

# Andrew Craighead
# December 4th, 2017
# Lab 3 Client

import socket, sys, json

print("My chat room client. Version One.")

# Setting up connection socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 13707))



while True:
	snd_msg = input(">")

	exit = snd_msg.split()[0]
	exit = exit.lower()
	# Client-side exit
	if exit == "exit" or exit == "quit" or exit == "q":
		sock.send("logout".encode())
		print(sock.recv(256).decode())
		break


	sock.send(snd_msg.encode())
	rcv_msg = sock.recv(256).decode()

	print(rcv_msg)

print("Closing connection")
sock.close()