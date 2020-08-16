# -*- coding: utf-8 -*-
#!/usr/bin/python
import pandas as pd
import sqlite3
from datetime import date
#connecting with the database.
db = sqlite3.connect("testing.db")
#db.execute("drop table if exists results")
db.execute("create table results(id int PRIMARY KEY,orderID text, Date datetime, vCode text,tCodes text,status text)")

def sq_lite3(vCode,tCodes,status,orderID):
#inserting values inside the created table
    db = sqlite3.connect("testing.db")    
    from datetime import date
    Date = date.today().strftime("%d-%m-%Y")
    status = 0    
    cmd = "insert into results(orderID, Date,vCode,tCodes,status) values('{}','{}','{}','{}','{}')".format(orderID,Date,vCode,tCodes,status)
    db.execute(cmd)
    db.commit()
#%%
import sqlite3
import pandas as pd
db = sqlite3.connect("testing.db")
qry = "SELECT * FROM results"
df = pd.read_sql_query(qry, db)
df.head()
