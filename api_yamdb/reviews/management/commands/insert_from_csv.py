import sqlite3 as lite
import sys
 
try:
    con = lite.connect('db.sqlite3')
    cur = con.cursor()  
    cur.executescript(f"INSERT INTO {TABLE_NAME} VALUES (?,?,?,?)")
    con.commit()
    
except lite.Error, e:
    if con:
        con.rollback()
        
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    if con:
        con.close()