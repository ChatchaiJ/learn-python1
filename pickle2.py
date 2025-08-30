import pickle
import struct
import socket

s = "HELLO WORLD"
l = len(s)

#	def send(channel, *args):
#	        buffer = pickle.dumps(args)
#	        value = socket.htonl(len(buffer))
#	        size = struct.pack("L", value)
#	        channel.send(size)
#	        channel.send(buffer)
#	
#	def receive(channel):
#	        size = struct.calcsize("L")
#	        size = channel.recv(size)
#	        try:
#	                size = socket.ntohl(struct.unpack("L", size)[0])
#	        except struct.error as e:
#	                return ''
#	        buf = ""
#	        while len(buf) < size:
#	                buf = channel.recv(size - len(buf))
#	        return pickle.loads(buf)[0]


print(f"s:'{s}', l:{l}")

buffer = pickle.dumps(s)
print(f"pickle.dumps(s) -> buffer='{buffer}'")

buffer2 = pickle.loads(buffer)
print(f"pickle.loads(buffer) -> buffer2='{buffer2}'")

size = struct.calcsize("L")
print(f"size={size}")
