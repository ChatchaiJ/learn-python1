#!/usr/bin/env python3

import socket
import sys

def reuse_socket_addr():
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	old_state = s.getsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR )
	print("old socket state: {}".format(old_state))

	s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
	new_state = s.getsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR )
	print("new socket state: {}".format(new_state))

	local_port = 8282
	srv = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	srv.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 0 )
	srv.bind( ('', local_port) )
	srv.listen(1)

	print("Listening on port: {}".format(local_port))

	while True:
		try:
			connection, addr = srv.accept()
			print("Connected by {}:{}".format(addr[0], addr[1]))
		except KeyboardInterrupt:
			break
		except socket.error as msg:
			print("{}".format(msg))

if __name__ == '__main__':
	reuse_socket_addr()
	
	
