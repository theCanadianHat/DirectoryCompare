#!/usr/bin/python
import walk 
import view 
import Tkinter as tk
import os

class Controller(object):
  def __init__(self):
    self.walk = walk.Walk()
    self.view = view.View(self)

  def search(self,dir1,dir2):
    if not(self.view.err == None):
      self.view.err.destroy()
    self.view.errSig = False
    if (dir1 == '') or (dir2 == ''):
      self.view.showError(1)
      self.view.errSig = True
    if not(os.path.isdir(dir1)) or not(os.path.isdir(dir2)):
      if not(os.path.isdir(dir1)) and not(os.path.isdir(dir2)):
        if not(self.view.errSig):
          self.view.showError(5)
      elif not(os.path.isdir(dir1)):
        self.view.showError(6)
      elif not(os.path.isdir(dir2)):
        self.view.showError(7)
    else:
      self.view.clearLists(0)
      self.walk.setupWalk(dir1, dir2)
      self.view.notifyLists(self.walk.getPaths(1),1)
      self.view.notifyLists(self.walk.getPaths(2),2)
      temp = self.walk.compareFiles(self.walk.getNames(1),self.walk.getNames(2))
      self.view.notifyLabels(temp)
 
  def compare(self,lhs,rhs):
    if (lhs == '') or (rhs == ''):
      self.view.showError(2)
    else:
      check = self.walk.sameFiles(lhs,rhs)
      if check:
        self.view.notifyEntry(3)
      if not check:
        self.view.notifyEntry(4)

  def rename(self,file,dest):
    if not(len(dest) == 0):
      self.view.r.destroy()
      self.walk.rename(file,dest)
    else:
      self.view.showError(3)

  def delete(self,file):
    self.view.d.destroy()
    self.walk.delete(file)

if __name__ == "__main__":
  controller = Controller()
  tk.mainloop()

