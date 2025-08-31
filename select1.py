#!/usr/bin/env python3

# Need some example code to show how select() work.
# It should show several source of inputs, maybe read from files, 
# one byte at a time, and delay between bytes

import sys
import time
import select

count = 0
f1 = open("/etc/passwd","r")
f2 = open("/etc/trafshow","r")

while True:
	b1 = f1.read(1)
	b2 = f2.read(1)
	time.sleep(0.1)
	print("={}/{}=".format(b1,b2))
	count = count + 1
	if count > 100:
		break

f1.close
f2.close

