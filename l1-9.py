#!/usr/bin/env python3

import socket

def	test_socket_modes():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setblocking(1)
	s.settimeout(0.5)
	s.bind(("127.0.0.1", 0))

	addr = s.getsockname()
	print("Trivial Server launched on socket: {}".format(addr))

	while True:
		s.listen(1)

if __name__ == '__main__':
	test_socket_modes()
