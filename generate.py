#!/usr/bin/python
# A program to generate directorys and
# files to test file maintenance programs.

import os
import sys
import gzip
import random

class Generator(object):
  def __init__(self, dir):
    self.startDir = dir
    self.noDirs = 0
    self.noFiles = 0
    self.newdir = dir
    self.pwd = os.getcwd() 
    self.words = []
    dict = gzip.open ('webster.txt.gz')
    for line in dict:
      self.words.append( line.rstrip('\n') )

  def __repr__(self):
    return "\tNew directory is "+self.startDir+'\n' \
    +"\tGenerated "+str(self.noDirs)+" Subdirectories" +'\n' \
    +"\tGenerated "+str(self.noFiles)+" Files" +'\n'

  def writeFile(self, filename):
    FILE = open(filename,"w")
    self.noFiles += 1
    n = random.randint(5,10)
    for x in range(1, n):
      w= random.randint(0, len(self.words))
      word = self.words[w]
      FILE.write(word)
      FILE.write(' ')
    FILE.write('\n')
    FILE.close()

  def makeFiles(self, extension):
    n = random.randint(3,7)
    for x in range(2,n):
      w = random.randint(0, len(self.words))
      name = self.words[w]
      newfile = name+extension
      self.writeFile(newfile)

  def generate(self):
    if os.path.isdir(self.newdir) or os.path.isfile(self.newdir):
      print self.newdir, \
        " already exists, choose a non-existing directory."
      return
    for x in range(1,4):
      os.mkdir(self.newdir)
      self.noDirs += 1
      os.chdir(self.newdir)
      if x == 3:
          self.writeFile("same.cpp")
      self.makeFiles('.pyc')
      self.makeFiles('.txt')
      n = random.randint(0, len(self.words))
      self.newdir = self.words[n]

    os.chdir(self.pwd)


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "usage: ", sys.argv[0], " <start dir>"
    sys.exit()
  generator = Generator(sys.argv[1])
  generator.generate()
  print generator
