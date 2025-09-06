#!/usr/bin/env python

import argparse
import sys
import socket
import fcntl
import struct
import array

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915, # SIOCGIFADDR
		struct.pack('256s', bytearray(ifname[:15], 'ascii'))
	)[20:24])

if __name__ == '__main__':
	# interface = list_interfaces()
	parser = argparse.ArgumentParser(description='Python networking utils')
	parser.add_argument('--ifname', action="store", dest="ifname", required=True)
	given_args = parser.parse_args()
	ifname = given_args.ifname
	print(f"Interface [{ifname}] --> IP: {get_ip_address(ifname)}")
