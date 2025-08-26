#!/usr/bin/env python3

import threading
import time

def	crawl(link, delay=3):
	print(f"crawl started for {link}")
	time.sleep(delay) # Blocking I/O (simulating a network request)
	print(f"crawl ended for {link}")

links = [
	"https://python.org",
	"https://docs.python.org",
	"https://peps.python.org",
]

threads = []
for link in links:
	# Using 'args' to pass positional arguments and 'kwargs' for keyword arguments
	t = threading.Thread(target=crawl, args=(link,), kwargs={"delay": 2})
	threads.append(t)

for t in threads:
	t.start()

for t in threads:
	t.join()
