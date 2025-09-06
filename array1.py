#!/usr/bin/env python3

import array

a = array.array('b', b"Hello World")
print(a)
a.append(0)
a.append(72)
print(a)

def	tostr(_):
	s = ''
	for i in _:
		if i==0:
			break
		s += chr(i)
	return s

print(f"{tostr(a)}")

