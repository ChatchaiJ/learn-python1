#!/usr/bin/env python3

import argparse
import socket
import errno
from time import time as now
from time import sleep

DEFAULT_TIMEOUT = 120
DEFAULT_SERVER_HOST = 'localhost'
DEFAULT_SERVER_PORT = 80

class NetServiceChecker(object):
	"""Wait for a network service to come online"""

	def __init__(self, host, port, timeout=DEFAULT_TIMEOUT):
		self.host = host
		self.port = int(port)
		self.timeout = timeout
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def end_wait(self):
		self.sock.close()

	def check(self):
		"""Check the service"""
		if self.timeout:
			end_time = now() + int(self.timeout)

		while True:
			sleep(1)
			try:
				if self.timeout:
					next_timeout = end_time - now()
					if next_timeout < 0:
						return False
					else:
						print(f"setting socket next timeout {round(next_timeout)}s")
						self.sock.settimeout(next_timeout)
				self.sock.connect( (self.host, self.port) )
			except socket.timeout as err:
				if self.timeout:
					return False
				else:
					self.end_wait()
					return True
			except socket.error as err:
				print(f"Exception: {err}")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Wait for Network Service')
	parser.add_argument('--host', action="store", dest="host", default=DEFAULT_SERVER_HOST)
	parser.add_argument('--port', action="store", dest="port", default=DEFAULT_SERVER_PORT)
	parser.add_argument('--timeout', action="store", dest="timeout", default=DEFAULT_TIMEOUT)
	given_args = parser.parse_args()
	host, port, timeout = given_args.host, given_args.port, given_args.timeout
	service_checker = NetServiceChecker(host, port, timeout=timeout)
	print(f"Checking for network service {host}:{port}")
	if service_checker.check():
		print("Service is available again!")
			
