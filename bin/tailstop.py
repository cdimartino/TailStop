#!/usr/bin/python

import sys
import re
import time
import os
import stat
import signal

class TailStop:
  def tail(self):
    file = open(self.filename)
    current_inode = os.stat(self.filename)[stat.ST_INO]

    while True:
      try:
        this_inode = None
        while not this_inode:
          this_inode = os.stat(self.filename)[stat.ST_INO]
          if this_inode != current_inode:
            sys.stderr.write("File changed - following by name\n")
            file = open(self.filename)
            current_inode = this_inode

        where = file.tell()
        line = file.readline()
        if not line:
          time.sleep(1)
          file.seek(where)
        else:
          matches = self.matcher(self.watch, line)
          if matches:
            i = 0
            for m in matches:
              self.write( line[i:m.start()] )
              self.write( self.color(line[m.start():m.end()]) )
              i = m.end()
            self.write(line[i:])

            cont = False
            while cont is False:
              response = raw_input("\nPlease press <enter> to continue, 'G' to go to end of file, or any phrase to change the match string: ")
              if response == "":
                cont = True
              elif response == "G":
                file.seek(0, os.SEEK_END)
                cont = True
              else:
                watch = response
          else:
            self.write(line)
      except KeyboardInterrupt:
        self.handle_change_watch()

  def matcher(self, which, target):
    matches = [m for m in re.finditer(which, target)]
    if len(matches):
      return matches
    return None

  def color(self, what):
    return "[0;31;40m%s[0;37;40m" % what

  def write(self, what):
    sys.stdout.write( what )

  def handle_change_watch(self):
    try:
      watch = raw_input("Enter <ctrl-c> again to quit.  Enter new search string: ")
      self.write("Setting new watch parameter to: %s\n" % watch)
      self.watch = watch
    except KeyboardInterrupt:
      sys.exit(0)

  def handler(self, signum, frame):
    self.handle_change_watch()

def main():
  ts = TailStop()
  ts.watch, ts.filename = sys.argv[1:3]
  ts.tail()

if __name__ == '__main__':
  main()
