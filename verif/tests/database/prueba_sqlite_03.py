# -*- coding: utf-8 -*-

import sqlite3 as sqlite
from sqliteUtils import macros_sqlite
from misc import ansysToEsfBarra

dbName= "/tmp/pilares.db"
import os
os.system("rm -f " + dbName)
macros_sqlite.SQLTcreaDBase(dbName)

conn= sqlite.connect(dbName)
cur= conn.cursor()
cur.execute("create table test3 ( num integer, name string );")
cur.execute("create table test4 ( A integer, B double );")
macros_sqlite.SQLTborraTabla(dbName,"test3")
macros_sqlite.SQLTborraTabla(dbName,"test4")
e1= macros_sqlite.SQLTexisteTabla(dbName,"test3")
e2= macros_sqlite.SQLTexisteTabla(dbName,"test4")



fname= os.path.basename(__file__)
if (not e1) & (not e2):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."

os.system("rm -f /tmp/pilares.db")
