#!/usr/bin/env python3

import socket

def get_remote_machine_info():
	remote_host = 'www.python.org'
	try:
		print("IP address: {}".format(socket.gethostbyname(remote_host)))
	except:
		print("{}: {}".format(remote_host, "Error"))
		exit(0)

if __name__ == "__main__":
	get_remote_machine_info()
