#!/usr/bin/env python3

import os
import sys
import time
import threading
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

class MyTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer, ):
	allow_reuse_address = True

with MyTCPServer( (SERVER_HOST, SERVER_PORT), ServerHandler) as server:
	try:

		ip, port = server.server_address
		server_thread = threading.Thread(target=server.serve_forever, daemon=False)
		server_thread.start()
		print(f"Server loop running PID: {os.getpid()} at {ip}:{port}")


		server_thread.join()
	

	except KeyboardInterrupt:
		print("\nServer shutting down")
		server.shutdown()
		sys.exit(0)
