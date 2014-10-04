#!/usr/bin/python
import sys, os
import stack
import filecmp as fc

class Walk(object):
  def __init__(self):
    #self.files = []
    #self.paths = {}
    self.filepaths1 = []
    self.fielpaths2 = []
    self.filesnames1 = []
    self.filesnames2 = []
  def printFiles(self):
    print "The", len(self.files), "are", self.files

  def walk(self,dir):
    stk = stack.stack()
    stk.push(dir)
    filepaths = []
    filenames = []
    while not stk.empty():
      directory = stk.top()
      stk.pop()  
      files = os.listdir(directory)
      for thisFile in files:
        filenames.append(thisFile)
        name = os.path.join(directory, thisFile)
        if not os.path.isdir(name):
          filepaths.append(name)
        if os.path.isdir(name):
          stk.push( name )
    retval = []
    retval.append(filepaths)
    retval.append(filenames)
    return retval

  def compareFiles(self,lhs,rhs):
    files = []
    for thing1 in lhs:
      for thing2 in rhs:
        if thing1 == thing2:
          files.append(thing1)
 
    text = "The files in common are:",files
    text += "There are",len(lhs),"files in the source directory"
    text +="There are",len(rhs),"files in the destination directory"
    if len(files) == 1:
      text += "They share",len(files),"file in common"
    if len(files) > 1: 
      text += "They share",len(files),"files in common"
    
    return files

  def setupWalk(self,dir1,dir2):
    temp = self.walk(dir1)
    self.filepaths1 = temp[0]
    self.filenames1 = temp[1]
    temp = self.walk(dir2)
    self.filepaths2 = temp[0]
    self.filenames2 = temp[1]

 
  def getPaths(self, d):
    if d == 1:
       return self.filepaths1
    else:
       return self.filepaths2

  def getNames(self, n):
    if n == 1:
      return self.filenames1
    else:
      return self.filenames2

  def sameFiles(self,lhs,rhs):
    check = fc.cmp(lhs,rhs)
    return check

  def rename(self,file,dest):
    if not os.path.isdir('RENAMED'):
      os.mkdir('RENAMED')
    os.rename(file,'RENAMED/'+dest)

  def delete(self,file):
    os.remove(file)


if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "usage:", sys.argv[0], "<dir> <dir>"
    sys.exit()
  dir1 = Walk(sys.argv[1])
  dir2 = Walk(sys.argv[2])
  commonFiles = dir1.compareFiles(dir2) 
  
  ans = raw_input("Would you like to compare the files for redundancy? (y/n) ")
  if ans == 'y':
    for files in commonFiles:
      path1 = dir1.paths[files]
      path2 = dir2.paths[files]

      if check:
        print "Files:\n"+dir1.paths[files]+"/"+files+"\n"+dir2.paths[files]+"/"+files+"\n"
        print "Are the same files"
      else:
        print "Files:\n"+dir1.paths[files]+"/"+files+"\n"+dir2.paths[files]+"/"+files+"\n"
        print "Are not the same files"

  else:
   sys.exit()
