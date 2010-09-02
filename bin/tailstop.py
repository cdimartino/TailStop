#!/usr/bin/python

import sys
import re
import time
import os

watch = sys.argv[1]
file = open(sys.argv[2])

while True:
  where = file.tell()
  line = file.readline()
  if not line:
    time.sleep(1)
    file.seek(where)
  else:
    print line,
    if re.search(watch, line):
      cont = False
      while cont is False:
        response = raw_input("Please press <enter> to continue, 'G' to go to end of file: ")
        if response == '':
          cont = True
        elif response == 'e':
          file.seek(0, os.SEEK_END)
