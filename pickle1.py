#!/usr/bin/env python3

import os
import sys
import pprint

import pickle

data = [ {'a': 'A', 'b': 2, 'c': 3.0} ]
print(f"DATA: {data}")

data_string = pickle.dumps(data)
print(f"PICKLE_DUMPS: {data_string}")

data = pickle.loads(data_string)
print(f"PICKLE_LOADS: {data}")
