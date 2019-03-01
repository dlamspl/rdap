#!/usr/bin/env python
from __future__ import print_function
import urllib
import sys

input = sys.argv[1]
with open(input, "rb") as f:
	data = f.read()
	print(data.encode("base64"), end='')
