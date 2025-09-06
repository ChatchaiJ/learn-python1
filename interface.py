#!/usr/bin/env python3

import sys
import socket
import fcntl
import struct
import array

SIOCGIFCONF = 0x8912	# from C library sockios.h
STRUCT_SIZE_32 = 32
STRUCT_SIZE_64 = 40
PLATFORM_32_MAX_NUMBER = 2**32
DEFAULT_INTERFACES = 8

def	split_array(arr, size):
	arrs = []
	while len(arr) > size:
		pice = arr[:size]
		arrs.append(pice)
		arr = arr[size:]
	arrs.append(arr)
	return arrs

	
def	tostr(_):
	s = ''
	for i in _:
		if i==0:
			break
		s += chr(i)
	return s

def list_interfaces():
	interfaces = []
	max_interfaces = DEFAULT_INTERFACES
	is_64bits = sys.maxsize > PLATFORM_32_MAX_NUMBER
	struct_size = STRUCT_SIZE_64 if is_64bits else STRUCT_SIZE_32
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while True:
		bytes = max_interfaces * struct_size
		interface_names = array.array('B', b'\0' * bytes)
		sock_info = fcntl.ioctl(
			sock.fileno(),
			SIOCGIFCONF,
			struct.pack('iL', bytes, interface_names.buffer_info()[0])
		)
		outbytes = struct.unpack('iL', sock_info)[0]
		if outbytes == bytes:
			max_interfaces *= 2
		else:
			break

	namestr = interface_names.tobytes()
	n = split_array(namestr, struct_size)

	for i in n:
		name = tostr(i)
		if name != '':
			interfaces.append(name)
	return interfaces

if __name__ == '__main__':
	interfaces = list_interfaces()
	print(f"This machine has {len(interfaces)} interfaces: {interfaces}")
