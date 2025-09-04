#!/usr/bin/env python3

import sys
import time
import errno
import socket

def	ConnectToServer(host, port, timeout=60):
	print(f"ConnnectToServer {host}, {port}, {timeout}")

	print(f"Create Socket")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(f"Settimeout = {timeout}")
	s.settimeout(timeout)

	try:
		s.connect( (host, port) )
	except socket.error as err:
		print(f"Error connect to {host}:{port} -- {err}")
		return
		# sys.exit(-1)
	except socket.timeout:
		print(f"Socket Timeout")
		return
		# sys.exit(-1)

	s.close()
	print(f"Connect to {host}:{port} success\n")
	
host = "turtle.cjv6.net"
port = 80
timeout = 3
ConnectToServer(host, port, timeout)

host = "localhost"
ConnectToServer(host, port, timeout)

host = "turtle.cjv6.net"
port = 2048
ConnectToServer(host, port, timeout)
