#!/usr/bin/env python3

import socket

def convert_integer(data):
	print("Original: {} => Long	host byte order: {}, network byte order: {}".
			format(data, socket.ntohl(data), socket.htonl(data)))
	print("Original: {} => Short	host byte order: {}, network byte order: {}".
			format(data, socket.ntohs(data), socket.htons(data)))
	print("\n")

if __name__ == '__main__':
	for i in range(1,10):
		convert_integer(i)

