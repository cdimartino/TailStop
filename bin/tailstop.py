#!/usr/bin/python

import sys
import re
import time
import os
import stat
import signal
import readline

class TailStop:
  def tail(self):
    file = open(self.filename)
    current_inode = os.stat(self.filename)[stat.ST_INO]

    stop = False
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
          if matches or stop:
            cont = False
            if matches:
              i = 0
              for m in matches:
                self.write( line[i:m.start()] )
                self.write( self.color(line[m.start():m.end()]) )
                i = m.end()
              self.write(line[i:])

            while cont is False:
              if stop == False:
                response = raw_input("\n<c>ontinue <e>nd <q>uit [<n>ext]: ")
              else:
                response = raw_input('->> ')

              if response == "c":
                cont = True
                stop = False
              elif response == "e":
                file.seek(1, 2)
                cont = True
                stop = False
                self.write(line)
              elif response == 'q':
                sys.exit(0)
              elif response == '':
                stop = True
                cont = True
                self.write(line)
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
      watch = raw_input("\nEnter <ctrl-c> again to quit.  Enter new search string: ")
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
