#!/usr/bin/env python3

import sys
import time
import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 9999

class ServerHandler(socketserver.BaseRequestHandler):
	"""
		Request handler 'class' for the server
	"""

	charset = [ b"ABCDEFGHIJKLMNOPQRSTUVWXYZ" + b"abcdefghijklmnopqrstuvwxyz" + b"0123456789" ]

	def	handle(self):

		print(f"Connected from {self.client_address[0]}")
		# just send back the same data but upper-cased
		while True:
			try:
				self.request.sendall(self.charset[0])
			except BrokenPipeError:
				print(f"Client {self.client_address} disconnected")
				break
			except Exception as e:
				print(f"An unexpected error occurred with {self.client_address}: {e}")
				break
			time.sleep(0.1)
		# after we return, the socket will be closed

class MyTCPServer(socketserver.TCPServer):
	allow_reuse_address = True

with MyTCPServer( (SERVER_HOST, SERVER_PORT), ServerHandler) as server:
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("\nServer shutting down")
		sys.exit(0)
