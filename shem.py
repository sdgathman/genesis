#!/usr/bin/python2

import csv

# possible anchors to compute BC dates
CARTHAGE = 814	
#CARTHAGE = 825	
REBUILD = 457
CHRISTMAS = 4

def toJul(am):
  bc = BC - am
  if bc > 0:
    return '%4dBC'%bc
  return '%4dAD'%(1-bc)

class event(object):
  def __init__(self,par,age,name,ref,comment = None,same=None):
    self.parent = par
    self.age = age
    self.name = name
    self.ref = ref
    self.comment = comment
    self.next = same

  def birthday(self):
    if not self.parent: return 0
    return self.age + self.parent.birthday()

  def indent(self):
    if not self.parent: return 0
    return self.parent.indent() + 1

  def __str__(self):
    AM = self.birthday()
    try:
      bc = toJul(AM)
    except:
      bc = '----BC'
    return '%4d %s'%(AM,bc)+' '*self.indent()+'%3d %s %s'%(
        self.age,self.name,self.ref)

def load(fp):
    "Adam,130,Seth,5:3"
    r = csv.reader(fp)
    h = r.next()    # header
    d = {}
    a = event(None,0,'Adam','1:7')
    d[a.name] = a
    p = a
    for row in r:
      while len(row) < 5:
        row.append('')
      par = row[0]
      if par.startswith('#'): continue
      n = row[1]
      age = int(n)
      if n.startswith('+'):
        age += lastage
      else:
        lastage = age
      name = row[2]
      ref = row[3] 
      if par:
        p = d[par]
      if not name:
        name = '~'+p.name
      if name in d:
        same = d[name]  # same event
      else:
        same = None
      cur = event(p,age,name,ref,row[4],same)
      d[name] = cur
      if same:
        try:
          assert same.birthday() == cur.birthday()
        except:
          print name,cur,same
    return d

with open('shem.dat','r') as fp:
    d = load(fp)
    BC = d['Carthage'].birthday() + CARTHAGE
    #BC = d['decree to rebuild Jerusalem'].birthday() + REBUILD
    #BC = d['Jesus'].birthday() + CHRISTMAS
    l = d.values()
    for e in l:
      n = e.next
      while n:
        l.append(n)
        n = n.next
    l.sort(key=lambda x: x.birthday())
    for v in l:
      print v
