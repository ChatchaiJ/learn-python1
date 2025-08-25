#!/usr/bin/env python

import os
import time
import socket
import threading
import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0	# tell the kernel to pick up a port dynamically
BUF_SIZE = 1024
ECHO_MSG =  'Hello Echo Server!'

class ForkedClient():
	"""A client to test forking server"""

	def __init__(self, ip, port):
		# Create a socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((ip, port))

	def run(self):
		""" Client playing with the server"""

		echo_msg = "{} -- Hello from echo client".format(time.asctime())
		# Send the data to server
		current_process_id = os.getpid()
		print("CLN: PID {} sending echo message to the server : {}".format(current_process_id, echo_msg))
		send_data_length = self.sock.send(echo_msg.encode('ascii'))
		print("CLN: Sent {:d} characters, so far ...".format(send_data_length))

		# Display server response
		response = self.sock.recv(BUF_SIZE).decode('ascii')
		print("CLN: PID {} received: {}".format(current_process_id, response))

	def shutdown(self):
		""" Cleanup the client socket """
		self.sock.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		# Send the echo back to the client
		data = self.request.recv(BUF_SIZE)
		current_process_id = os.getpid()
		response = '{}: {}'.format(current_process_id, data.decode('ascii'))
		print("SVR: Server sending response[current_process_id: data] = [{}]".format(response))
		self.request.send(response.encode('ascii'))
		return

class ForkingServer(socketserver.ForkingMixIn,
					socketserver.TCPServer,
					):
	"""Nothing to add here, inherited everything necessary from parents"""
	pass

def main():
	# Launch the server
	server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)

	ip, port = server.server_address # Retreive the port nummber
	server_thread = threading.Thread(target=server.serve_forever, daemon=True)
#	server_thread.setDaemon(True) # don't hang on exit
	server_thread.start()
	print("SVR: Server loop running PID: {}".format(os.getpid()))

	# Launch the client(s)
	print("MAIN: fork client 1")
	client1 = ForkedClient(ip, port)
	client1.run()

	print("MAIN: fork client 2")
	client2 = ForkedClient(ip, port)
	client2.run()

	# Clean them up
	print("MAIN: shutdown server")
	server.shutdown()

	print("MAIN: shutdown client 1")
	client1.shutdown()

	print("MAIN: shutdown client 2")
	client2.shutdown()
	server.socket.close()

if __name__ == '__main__':
	main()
