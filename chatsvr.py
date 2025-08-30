#!/usr/bin/env python3

import sys
import select
import socket
import signal
import pickle
import struct
import argparse

SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'

# some utilities
def send(channel, *args):
	buffer = pickle.dumps(args)
	value = socket.htonl(len(buffer))
	size = struct.pack("L", value)
	channel.send(size)
	channel.send(buffer)

def receive(channel):
	size = struct.calcsize("L")
	size = channel.recv(size)
	try:
		size = socket.ntohl(struct.unpack("L", size)[0])
	except struct.error as e:
		return ''
	buf = ""
	while len(buf) < size:
		buf = channel.recv(size - len(buf))
	return pickle.loads(buf)[0]

class ChatServer(object):
	""" An example chat server using select """
	def __init__(self, port, backlog=5):
		self.clients = 0
		self.clientmap = {}
		self.outputs = [] # list of output sockets
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Enable re-using socket address
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind( (SERVER_HOST, port) )

		print(f"Server listening to port: {port} ...")
		self.server.listen(backlog)

	def sighandler(self, signum, frame):
		"""clean up client outputs"""

		# Close the server
		print("Shutting down server...")
		for output in self.outputs:
			output.close()

		self.server.close()

	def	get_client_name(self, client):
		"""Return the name of the client"""
		info  = self.clientmap[client]
		host, name = info[0][0], info[1]
		return '@'.join((name, host))	

	def run(self):
		inputs = [self.server, sys.stdin]
		self.outputs = []
		running = True
		while running:
			try:
				readable, writeable, exceptional = select.select(inputs, self.outputs, [])
			except select.error as e:
				break
			for sock in readable:
				if sock == self.server:
					# handle the server socket
					client, address = self.server.accept()
					print(f"Chat server: got connection {client.fileno()} from {address}")

					# Read the login name
					cname = receive(client).split('NAME: ')[1]

					# Compute client name and send back
					self.clients += 1
					send(client, 'CLIENT: ' + str(address[0]))
					inputs.append(client)
					self.clientmap[client] = (address, cname)

					# Send joining informaton to other clients
					msg = f"\n(Connected: New client ({self.clients}) from {self.get_client_name(client)})"

					for output in self.outputs:
						send(output, msg)

					self.outputs.append(client)

				elif sock == sys.stdin:
					# handle standard input
					junk = sys.stdin.readline()
					running = False

				else:
					# handle all other sockets
					try:
						data = receive(sock)
						if data:
							# Send as new clients' message...

##							print(f"DEBUG: client{sock} => {data()}")
## DEBUG: client<socket.socket fd=5, family=2, type=1, proto=0, laddr=('127.0.0.1', 9900), raddr=('127.0.0.1', 37832)> => hello

							print(f"DEBUG: client{sock.fileno()} => {data()}")
							msg = f"\n#[{self.get_client_name(sock)}]>> " + str(data())

							# Send data to all except ourself
							for output in self.outputs:
								if output != sock:
									send(output, msg)
						else:
							print(f"Chat server: {sock.fileno()} hung up")
							self.clients -= 1
							sock.close()
							inputs.remove(sock)
							self.outputs.remove(sock)

							# Sending client leaving info to others
							msg = f"\n(Now hung up: Client from {self.get_client_name(sock)}"
							for output in self.outputs:
								send(output, msg)
					except socket.error as e:
						# Remove
						inputs.remove(sock)
						self.outputs.remove(sock)

		self.server.close()

class ChatClient(object):
	"""A command line chat client using select"""

	def	__init__(self, name, port, host=SERVER_HOST):
		self.name = name
		self.connected = False
		self.host = host
		self.port = port

		# Initital prompt
		self.prompt='[' + '@'.join( (name, socket.gethostname().split('.')[0])) + ']> '

		# Connect to server at port
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect( (host, self.port) )
			print(f"Now connected to chat server @ port {self.port}")
			self.connected = True

			# Send my name ...
			send(self.sock, 'NAME: ' + self.name)
			data = receive(self.sock)

			# Contains client address, set it
			addr = data.split('CLIENT: ')[1]
			self.prompt = '[' + '@'.join( (self.name, addr) ) + ']> '
		except socket.error as e:
			print(f"Failed to connect to chat server @ port {self.port}")
			sys.exit(1)

	def run(self):
		"""Chat client main loop"""
		while self.connected:
			try:
				sys.stdout.write(self.prompt)
				sys.stdout.flush()

				# Wait for input from stdin and socket
				readable, writeable, exceptional = select.select([0, self.sock], [], [])
				for sock in readable:
					if sock == 0:
						data = sys.stdin.readline().strip
						if data:
							send(self.sock, data)
					elif sock == self.sock:
						data = receive(self.sock)
						if not data:
							print(f"Client shutting down.")
							self.connected = False
							break
						else:
							sys.stdout.write(data + '\n')
							sys.stdout.flush()
			except KeyboardInterrupt:
				print(f"Client interrupted")
				self.sock.close()
				break

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Socket Server Example with Select')
	parser.add_argument('--name', action="store", dest="name", required=True)
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	given_args = parser.parse_args()
	port = given_args.port
	name = given_args.name
	if name == CHAT_SERVER_NAME:
		server = ChatServer(port)
		server.run()
	else:
		client = ChatClient(name=name, port=port)
		client.run()
