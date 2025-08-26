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

	def __init__(self, ip, port, id):
		# Create a socket
		self.id = id
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((ip, port))

	def run(self):
		""" Client playing with the server"""

		for i in range(1,10):
			echo_msg = "ECHO {}: {}".format(i,time.asctime())
			# Send the data to server
			current_process_id = os.getpid()
			print("CLN{}: PID {} -snd- {}".format(self.id, current_process_id, echo_msg))
			send_data_length = self.sock.send(echo_msg.encode('ascii'))
			print("CLN{}: Sent {:d} characters, so far ...".format(self.id, send_data_length))

			# Display server response
			response = self.sock.recv(BUF_SIZE).decode('ascii')
			print("CLN{}: PID {} -rec- {}".format(self.id, current_process_id, response))
			time.sleep(1)

	def shutdown(self):
		""" Cleanup the client socket """
		self.sock.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		while True:
			# Send the echo back to the client
			data = self.request.recv(BUF_SIZE)
			current_process_id = os.getpid()
			response = '{}'.format(data.decode('ascii'))
			print("SVR: Server -- {}".format(response))
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
	print("MAIN: client 1")
	client1 = ForkedClient(ip, port, 1)
	cln1_thread = threading.Thread(target=client1.run)
	cln1_thread.start()

	print("MAIN: client 2")
	client2 = ForkedClient(ip, port, 2)
	cln2_thread = threading.Thread(target=client2.run)
	cln2_thread.start()

	# Wait for both clients to finish
	cln1_thread.join()
	cln2_thread.join()

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
