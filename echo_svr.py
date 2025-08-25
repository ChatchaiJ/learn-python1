#!/usr/bin/env python

import sys
import time
import socket
import argparse

host = 'localhost'
data_payload = 2048
backlog = 5

def echo_server(port):
	"""A simple echo server"""
	# Create a TCP socket

	sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
	server_address = (host, port)

	print("Starting up echo server on {} port {}".format(host, port))

	sock.bind(server_address)
	sock.listen(backlog)

	while True:
		print("===== {} =====".format(time.asctime()))
		print("Waiting to receive message from client")
		client, address = sock.accept()
		data = client.recv(data_payload)
		if data:
			print("{} -- Data: {}".format(time.strftime("%H:%M:%S"),data))
			time.sleep(2)
			client.send(data)
			print("{} -- Sent: {} => back to {}".format(time.strftime("%H:%M:%S"),data, address))
		client.close()
		print("----- {} -----\n".format(time.asctime()))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Socket Server Example")
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	given_args = parser.parse_args()
	port = given_args.port
	echo_server(port)
	
