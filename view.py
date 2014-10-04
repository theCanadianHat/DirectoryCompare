
#!/usr/bin/python
import sys
import Tkinter as tk
import os

TITLE = "Directory Manager"

ROOT_W = '700x'
ROOT_H = '450+'
ROOT_X = '200+'
ROOT_Y = '100'
ROOT_GEOMETRY = ROOT_W+ROOT_H+ROOT_X+ROOT_Y

RD_W = '400x'
RD_H = '150+'
RD_X = '350+'
RD_Y = '250'
RD_GEOMETRY = RD_W+RD_H+RD_X+RD_Y

HELP_W = '400x'
HELP_H = '360+'
HELP_X = '350+'
HELP_Y = '145'
HELP_GEOMETRY = HELP_W+HELP_H+HELP_X+HELP_Y

LIST_W = '300x'
LIST_H = '450+'
LIST_X = '900+'
LIST_Y = '100'
LIST_GEOMETRY = LIST_W+LIST_H+LIST_X+LIST_Y

class View(object):
  def __init__(self, controller):
    ''' The view has access to the controller so it can
        relay commands obtained from the gui to the controller '''
    self.controller = controller
    self.compare1 = ''
    self.compare2 = ''
    self.dr = ''
    self.errSig = False
    self.err = None
    self.l = None
    self.root = tk.Tk()
    self.root.geometry(ROOT_GEOMETRY)
    self.root.title(TITLE)
    self.root.bind('<Escape>',(lambda event: sys.exit()))

    row1 = tk.Frame(self.root)
    lab1 = tk.Label(row1, width=40, text='Source Directory')
    lab2 = tk.Label(row1, width=40, text='Destenation Directory')
    lab1.pack(side=tk.LEFT)
    lab2.pack(side=tk.RIGHT)
    row1.pack(side=tk.TOP)

    row2 = tk.Frame(self.root)
    src = tk.StringVar()
    dest = tk.StringVar()
    self.srcEntry = tk.Entry(row2,textvariable=src,width=41)
    self.srcEntry.pack(side=tk.LEFT)
    self.destEntry = tk.Entry(row2,textvariable=dest,width=41)
    self.destEntry.pack(side=tk.LEFT)
    row2.pack(side=tk.TOP)

    row3 = tk.Frame(self.root)
    row3l = tk.Frame(row3)
    row3r = tk.Frame(row3)
    scrollbarly = tk.Scrollbar(row3l)
    scrollbarry = tk.Scrollbar(row3r)
    scrollbarlx = tk.Scrollbar(row3l,orient=tk.HORIZONTAL)
    scrollbarrx = tk.Scrollbar(row3r,orient=tk.HORIZONTAL)
    
    scrollbarly.pack(side=tk.RIGHT,fill=tk.Y)
    scrollbarry.pack(side=tk.RIGHT,fill=tk.Y)
    scrollbarlx.pack(side=tk.BOTTOM,fill = tk.X)
    scrollbarrx.pack(side=tk.BOTTOM,fill = tk.X)
    #print root.width
    self.listb1 = tk.Listbox(row3l,xscrollcommand=scrollbarlx.set,yscrollcommand=scrollbarly.set,width = 40)
    self.listb2 = tk.Listbox(row3r,xscrollcommand=scrollbarrx.set,yscrollcommand=scrollbarry.set,width = 40)
    self.listb1.bind('<Double-1>',(lambda event=1:self.notifyEntry(1)))
    self.listb2.bind('<Double-1>',(lambda event=1:self.notifyEntry(2)))
    self.listb1.config(xscrollcommand=scrollbarlx.set,yscrollcommand=scrollbarly.set)
    self.listb2.config(xscrollcommand=scrollbarrx.set,yscrollcommand=scrollbarry.set)
    scrollbarly.config(command = self.listb1.yview)
    scrollbarlx.config(command = self.listb1.xview)
    scrollbarry.config(command = self.listb2.yview)
    scrollbarrx.config(command = self.listb2.xview)
    self.listb1.pack()
    self.listb2.pack()
    row3l.pack(side=tk.LEFT)
    row3r.pack(side=tk.RIGHT)
    row3.pack(side=tk.TOP)

    self.lab3 = tk.Label(self.root,width='100',height=5)
    self.lab3.config(text='Comparison Info')
    self.lab3.pack(side=tk.TOP)

    row5 = tk.Frame(self.root)
    button = tk.Button(row5, text="Help", width=10,bg='blue') 
    button.configure(command=self.showHelp)
    button.pack(side=tk.LEFT)

    button = tk.Button(row5, text="Search", width=10,bg='green') 
    button.configure(command=(lambda t=1:self.controller.search(src.get(),dest.get())))
    button.pack(side=tk.LEFT)

    button = tk.Button(row5, text="Clear", width=10,bg='yellow') 
    button.configure(command=(lambda e=1:self.clearLists(1)))
    button.pack(side=tk.LEFT)

    button = tk.Button(row5, text="Quit", width=10,bg = 'red') 
    button.configure(command=sys.exit)
    button.pack(side=tk.LEFT)
    row5.pack(side=tk.TOP)

    bar2=tk.Frame(self.root,height=3,width=700,relief='sunken',pady=10)
    bar2.pack()
    bar=tk.Frame(self.root,height=3,width=700,bg="black",relief='sunken',pady=10)
    bar.pack()
    bar1=tk.Frame(self.root,height=3,width=700,relief='sunken',pady=10)
    bar1.pack()

    row6 = tk.Frame(self.root)
    
    row6l = tk.Frame(row6,bd = 3)
    r6LLF = tk.LabelFrame(row6l,text = 'Compare')
    self.ent1 = tk.Label(r6LLF,text='Compare Entry 1',width=40,relief='sunken',bg='gray')
    self.ent2 = tk.Label(r6LLF,text='Compare Entry 2',width=40,relief='sunken',bg='gray')
    button = tk.Button(r6LLF, text="Compare", width=10) 
    button.configure(command=(lambda e=1:self.controller.compare(self.compare1,self.compare2)))
    self.ent1.pack(side=tk.TOP,anchor=tk.W)
    button.pack()
    self.ent2.pack(side=tk.TOP,anchor=tk.W)
    self.compInfo = tk.Label(r6LLF,width=40,bg='black',relief='sunken',fg='red')
    self.compInfo.pack(anchor=tk.W)
    
    row6r = tk.Frame(row6,bd = 3)
    r6RLF = tk.LabelFrame(row6r,text = 'Reaname/Delete')
    button = tk.Button(r6RLF, text="Rename", width=10) 
    button.configure(command=(lambda e=1:self.rename(self.dr)))
    button.pack()
    self.ent3 = tk.Label(r6RLF,bg='gray',text='Rename/Delete Entry 3',width=40,relief='sunken')
    self.ent3.pack()
    button = tk.Button(r6RLF, text="Delete", width=10)
    button.configure(command=self.showDelete)
    button.pack()

    r6LLF.pack()
    r6RLF.pack()
    row6l.pack(side=tk.LEFT)
    row6r.pack(side=tk.RIGHT)
    row6.pack(side=tk.TOP)

  def notifyLists(self,L,n):
    if n == 1:
      for thing in L:
        self.listb1.insert(tk.END,thing)
    else:
      for thing in L:
        self.listb2.insert(tk.END,thing)

  def notifyLabels(self,files):
    empty = False
    if len(files) == 0:
       empty = True
    #l1 = "The files in common are: %s" %(files)
    self.showList(files)
    l2 = "There are %d files in the source directory" %(len(self.controller.walk.getNames(1)))
    l3 = "There are %d files in the destination directory" %(len(self.controller.walk.getNames(2)))
    if not empty:
      if len(files) == 1:
        l4 = "They share %d file in common" %(len(files))
      if len(files) > 1: 
        l4 = "They share %d files in common" %(len(files))
    if empty:
      l4 = "They share no files in common"
    temp = '%s\n%s\n%s' %(l2,l3,l4)
    self.lab3.config(text=temp)

  def notifyEntry(self,n):
    if n == 1:
      index = self.listb1.curselection()
      text = self.listb1.get(index)
      self.ent1.config(text=text,bg='gray',fg='black')
      self.ent2.config(bg='gray',fg='black')
      self.ent3.config(text=text)
      self.compInfo.config(fg='black',text='')
      self.compare1 = text
      self.dr = text
    if n == 2:
      index = self.listb2.curselection()
      text = self.listb2.get(index)
      self.ent1.config(bg='gray',fg='black')
      self.ent2.config(text=text,bg='gray',fg='black')
      self.compInfo.config(fg='black',text='')
      self.ent3.config(text=text)
      self.compare2 = text
      self.dr = text
    if n == 3:
      self.ent1.config(bg='green',fg='white')
      self.ent2.config(bg='green',fg='white')
      self.compInfo.config(fg='green',text='These files are the same!!!')
    if n == 4:
      self.ent1.config(bg='red',fg='white')
      self.ent2.config(bg='red',fg='white')
      self.compInfo.config(fg='red',text='These files are not the same!!!')

  def clearLists(self,n):
    if n == 0:
      self.listb1.delete(0, tk.END)
      self.listb2.delete(0, tk.END)
      self.lab3.config(text='Comparison Info')
      self.ent1.config(text='Compare Entry 1',bg='gray',fg='black')
      self.ent2.config(text='Compare Entry 2',bg='gray',fg='black')
      self.ent3.config(text='Rename/Delete Entry 3')
      self.compInfo.config(text='')
      self.compare2 = ''
      self.compare1 = ''
      self.dr = ''
      
    if n == 1:
      self.listb1.delete(0, tk.END)
      self.listb2.delete(0, tk.END)
      self.lab3.config(text='Comparison Info')
      self.ent1.config(text='Compare Entry 1',bg='gray',fg='black')
      self.ent2.config(text='Compare Entry 2',bg='gray',fg='black')
      self.ent3.config(text='Rename/Delete Entry 3')
      self.compInfo.config(text='')
      self.srcEntry.delete(0,tk.END)
      self.destEntry.delete(0,tk.END)
      self.compare2 = ''
      self.compare1 = ''
      self.dr = ''
      if not(self.l == None): self.l.destroy()

  def rename(self,file):
    self.r = tk.Toplevel(self.root)
    self.r.geometry(RD_GEOMETRY)
    self.r.title('Director Manager - Rename')
    rows = []
    row1 = tk.Frame(self.r)
    row2 = tk.Frame(self.r)
    row3 = tk.Frame(self.r)
    rows.append(row1)
    rows.append(row2)
    rows.append(row3)
    ok = tk.Button(row2,text='OK',bg = 'green')
    can = tk.Button(row2,text='Cancel',bg = 'red')

    if file == '':
      quest = "Please make sure the Rename entry is valid"
      ok.configure(command=self.r.destroy)
    else:
      quest = "What would you like to rename %s" %(file)
      dest = ''
      ent = tk.Entry(row2)
      ok.configure(command=(lambda e=1:self.controller.rename(file,ent.get())))
      can.configure(command=self.r.destroy)

    lab = tk.Label(row1,text=quest)
    lab.pack()
    if not(file == ''): 
      ent.pack()
      can.pack(side=tk.LEFT)

    ok.pack(side=tk.RIGHT)
    for row in rows:
      row.pack()

  def showHelp(self):
    window = tk.Toplevel(self.root)
    window.geometry(HELP_GEOMETRY)
    window.title('Directory Manager - Help')
    help = open('HELP.txt','r')
    row1 = tk.Frame(window) 
    sby = tk.Scrollbar(row1)
    lb = tk.Listbox(row1,width=45,height=20,yscrollcommand=sby.set)
    for line in help:
      lb.insert(tk.END,line[0:-1])
    sby.config(command=lb.yview)
    lb.pack(side=tk.LEFT)
    sby.pack(side=tk.RIGHT,fill=tk.Y)

    row2 = tk.Frame(window)
    ok = tk.Button(row2,text='OK',bg='green')
    ok.configure(command=window.destroy)
    ok.pack()
    
    row1.pack()
    row2.pack()

  def showDelete(self):    
    if not(self.dr == ''):
      self.d = tk.Toplevel(self.root)
      self.d.geometry(RD_GEOMETRY)
      self.d.title('Directory Manager - Delete')

      quest = "Are you sure you want to DELETE: %s" %(self.dr)

      row1 = tk.Frame(self.d)
      label = tk.Label(row1,text=quest,wraplength = 5)
      label.pack()

      row2 = tk.Frame(self.d)
      ok = tk.Button(row2,text='OK',bg='red')
      ok.configure(command=(lambda e=1:self.controller.delete(self.dr)))
      ok.pack(side=tk.RIGHT)
      cancel = tk.Button(row2,text='Cancel',bg='green')
      cancel.configure(command=self.d.destroy)
      cancel.pack(side=tk.LEFT)
      row1.pack()
      row2.pack()
    else:
     self.showError(4)

  def showError(self,n):
    if n == 1 or n == 2 or n == 4 or n==5 or n==6 or n==7:
      self.err = tk.Toplevel(self.root)
    if n == 3:
      self.err = tk.Toplevel(self.r)
      
    self.err.geometry(RD_GEOMETRY)
    self.err.title('Directory Manager - Error')
    row1 = tk.Frame(self.err)
    row2 = tk.Frame(self.err)
    
    if n == 1:
      label = tk.Label(row1,text='Please make sure BOTH Source and Destination feilds are valid!')
    if n == 2:
      label = tk.Label(row1,text='Please make sure BOTH Compare feilds are valid!')
    if n == 3:
      label = tk.Label(row1,text='Please provide a name for the file!')
    if n == 4:
      label = tk.Label(row1,text='Please make sure the Delete entry is valid!') 
    if n == 5:
      label = tk.Label(row1,text='Could not find EITHER Source or Destination Directories')
    if n == 6:
      label = tk.Label(row1,text='Could not find the SOURCE Directory')
    if n == 7:
      label = tk.Label(row1,text='Could not find the DESTINATION Directory')

    button = tk.Button(row2,text='OK',bg='green')
    button.configure(command = self.err.destroy)
    label.pack()
    row1.pack()
    button.pack()
    row2.pack()

  def showList(self,files):
    i =1
    if not(self.l == None):
       self.l.destroy()
    if len(files) > 0:
      self.l = tk.Toplevel(self.root)
      self.l.geometry(LIST_GEOMETRY)
      r1LF = tk.LabelFrame(self.l,text='Common Files')
      row1 = tk.Frame(r1LF)
      sb = tk.Scrollbar(r1LF)
      self.LB = tk.Listbox(r1LF,width=30,height=24,yscrollcommand = sb.set)
      sb.configure(command = self.LB.yview)
      sb.pack(side=tk.RIGHT,fill=tk.Y)
      self.LB.pack(side=tk.LEFT)
      for file in files:
        num = str(i)
        self.LB.insert(tk.END,'('+num+') '+file)
        i +=1
      row2 = tk.Frame(self.l)
      ok = tk.Button(row2,text='OK',bg='green')
      ok.configure(command=self.l.destroy)
      ok.pack()
      row1.pack()
      r1LF.pack(side=tk.TOP)
      row2.pack(side=tk.TOP)
