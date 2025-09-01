#!/usr/bin/env python3

import os
import argparse
import socket
import struct
import select
import time

ICMP_ECHO_REQUEST = 8
DEFAULT_TIMEOUT = 2
DEFAULT_COUNT = 4

class Pinger(object):
	"""Pings to a host -- the pythonic way"""

	def __init__(self, target_host, count=DEFAULT_COUNT, timeout=DEFAULT_TIMEOUT):
		self.target_host = target_host
		self.count = count
		self.timeout = timeout

	def do_checksum(self, source_string):
		"""Verify the packet integrity"""

		sum = 0
		max_count = (len(source_string)/2)*2
		count = 0

		while count < max_count:
#			val = ord(source_string[count + 1])*256 + ord(source_string[count])
			val = source_string[count + 1]*256 + source_string[count]
			sum = sum + val
			sum = sum & 0xFFFFFFFF
			count = count + 2

		if max_count < len(source_string):
			sum = sum + source_string[len(source_string) - 1]
			sum = sum & 0xFFFFFFFF

		sum = (sum >> 16) + (sum & 0xFFFF)
		sum = sum + (sum >> 16)
		answer = ~sum
		answer = answer & 0xFFFF
		answer = (answer >> 8) | ((answer << 8) & 0xFF00)

		return answer

	def receive_pong(self, sock, ID, timeout):
		"""Receive ping from socket"""

		time_remaining = timeout
		while True:
			start_time = time.time()
			readable = select.select([sock], [], [], time_remaining)
			time_spent = (time.time() - start_time)
			if readable[0] == []: # Timeout
				return

			time_received = time.time()
			recv_packet, addr = sock.recvfrom(1024)
			icmp_header = recv_packet[20:28]

			type, code, checksum, packet_ID, sequence = struct.unpack( "bbHHh", icmp_header )
			if packet_ID == ID:
				bytes_in_double = struct.calcsize("d")
				time_sent = struct.unpack("d", recv_packet[28:28 + bytes_in_double])[0]
				return time_received - time_sent

			time_remaining = time_remaining - time_spent
			if time_remaining <= 0:
				return

	def send_ping(self, sock, ID):
		"""Send ping to the target host"""

		target_addr = socket.gethostbyname(self.target_host)
		my_checksum = 0

		# Create a dummy header with a 0 checksum.
		header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
		bytes_in_double = struct.calcsize("d")
		data = (192 - bytes_in_double) * "Q"
		data = struct.pack("d", time.time()) + data.encode('ascii')

		# Get the checksum on the data and the dummy header.
		my_checksum = self.do_checksum(header + data)
		header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
		packet = header + data
		sock.sendto(packet, (target_addr, 1))

	def ping_once(self):
		"""Returns the delay (in seconds) or none on timeout"""

		icmp = socket.getprotobyname("icmp")
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
		except socket.error as errno:
			if errno == 1:
				# Not superuser, so operation is not permitted
				msg = "ICMP messages can only be sent from root user processes"
				raise socket.error(msg)
		except Exception as e:
			print(f"Exception: {e}")
		except:
			sys.exit(0)

		sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
		my_ID = os.getpid() & 0xFFFF
		self.send_ping(sock, my_ID)
		delay = self.receive_pong(sock, my_ID, self.timeout)
		sock.close()
		return delay

	def ping(self):
		"""Run the ping process"""

		for i in range(self.count):
			print(f"Ping to {self.target_host}...")
			try:
				delay = self.ping_once()
			except socket.gaierror as e:
				print(f"Ping failed. (socket error: {e[1]}")
				break

			if delay == None:
				print(f"Ping failed. (timeout within {self.timeout}s")
			else:
				delay = delay * 1000
				print(f"Get pong in {delay:0.4f}ms")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Python ping')
	parser.add_argument('--target-host', action="store", dest="target_host", required=True)
	given_args = parser.parse_args()
	target_host = given_args.target_host
	pinger = Pinger(target_host=target_host)
	pinger.ping()
	
