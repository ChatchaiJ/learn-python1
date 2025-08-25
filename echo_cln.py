#!/usr/bin/env python3

import sys
import time
import socket
import argparse

host = 'localhost'

def echo_client(port):
	"""A Simple echo client"""
	sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	server_address = (host, port)
	print("Connecting to {} port {}".format(host, port))
	sock.connect(server_address)

	try:
		message = """
    A robot may not injure a human being or, through inaction, allow a human being to come to harm.
    A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.
    A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.
	""".encode('ascii')
		print("{} -- Sending: {}".format(time.strftime("%H:%M:%S"),message))
		sock.sendall(message)
		amount_received = 0
		amount_expected = len(message)
	
		while amount_received < amount_expected:
			data = sock.recv(32)
			amount_received += len(data)
			print("{} -- Received: {}".format(time.strftime("%H:%M:%S"),str(data)))
			time.sleep(0.1)

#	except socket.errno as errno:
#		print("Socket error: {}".format(errno))
	except Exception as e:
		print("Other exception: {}".format(e))
	finally:
		print("Closing connection to the server")
		sock.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Socket Client Example")
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	given_args = parser.parse_args()
	port = given_args.port
	echo_client(port)
