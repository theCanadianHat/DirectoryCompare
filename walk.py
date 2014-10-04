#!/usr/bin/python

import sys, os
import stack
import filecmp as fc

class Walk(object):
  def __init__(self, dir):
    self.startDir = dir
    self.files = []
    self.paths = {}
    self.walk()

  def printFiles(self):
    print "The", len(self.files), "are", self.files

  def walk(self):
    stk = stack.stack()
    stk.push(self.startDir)
    while not stk.empty():
      directory = stk.top()
      stk.pop()
      files = os.listdir(directory)
      for thisFile in files:
          name = os.path.join(directory, thisFile)
          if os.path.isdir(name):
            stk.push( name )
          else:
            self.files.append( thisFile )
            self.paths.update({thisFile:directory})

  def compareFiles(self,rhs):
    self.files.sort()
    rhs.files.sort()
    files = []
    for thing1 in self.files:
      for thing2 in rhs.files:
        if thing1 == thing2:
          files.append(thing1)
 
    print "The files in common are:",files
    print "There are",len(self.files),"files in the source directory"
    print "There are",len(rhs.files),"files in the destination directory"
    if len(files) == 1:
      print "They share",len(files),"file in common"
    if len(files) > 1: 
      print "They share",len(self.files),"files in common"
    return files

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "usage:", sys.argv[0], "<dir> <dir>"
    sys.exit()
  dir1 = Walk(sys.argv[1])
  dir2 = Walk(sys.argv[2])
  #print dir1.paths
  #print dir2.paths

  #dir1.printFiles()
  #dir2.printFiles()

  commonFiles = dir1.compareFiles(dir2) 
  
  ans = raw_input("Would you like to compare the files for redundancy? (y/n) ")
  if ans == 'y':
    for files in commonFiles:
      path1 = dir1.paths[files]
      path2 = dir2.paths[files]
      print path1
      print path2
      check = fc.cmp(path1+'/'+files,path2+'/'+files)

      if check:
        print "Files:\n"+dir1.paths[files]+"/"+files+"\n"+dir2.paths[files]+"/"+files+"\n"
        print "Are the same files"
      else:
        print "Files:\n"+dir1.paths[files]+"/"+files+"\n"+dir2.paths[files]+"/"+files+"\n"
        print "Are not the same files"

  else:
   sys.exit()
