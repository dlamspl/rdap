#!/usr/bin/env python
from __future__ import print_function
import urllib
import sys

input = sys.argv[1].replace("'",'"')
parms = {'config':input}
print(urllib.urlencode(parms), end='')


