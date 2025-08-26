#!/usr/bin/env python3

import os
import socket
import threading
import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUF_SIZE = 1024

def client(ip, port, message):
	"""A client to test threading mixing server"""
	# Connect to the server
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect( (ip, port) )
	try:
		sock.sendall(message.encode('ascii'))
		response = sock.recv(BUF_SIZE)
		print(f"Client received: {response}")
	finally:
		sock.close()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	"""An example of threaded TCP request handler"""
	def handle(self):
		data = self.request.recv(BUF_SIZE).decode('ascii')
		current_thread = threading.current_thread()
		response = f"{current_thread.name}: {data}"
		self.request.sendall(response.encode('ascii'))

class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	"""Nothing to add here, inherited everything necessary from parents"""
	pass

if __name__ == '__main__':
	# Run server
	server = ThreadTCPServer( (SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address	# retrieve ip address

	# Start a thread with the server -- one thread per request
	server_thread = threading.Thread(target=server.serve_forever)

	# Exit the server thread when the main thread exists
	server_thread.daemon = True
	server_thread.start()
	print(f"Server loop running on thread: {server_thread.name}")

	# Run clients
	client(ip, port, "Hello from client 1")
	client(ip, port, "Hello from client 2")
	client(ip, port, "Hello from client 3")
	client(ip, port, "Hello from client 4")

	# Server cleanup
	server.shutdown()
