import pandas as pd
import json
import requests
import os 
import sqlite3
from datetime import date

os.system("curl 'https://api.gdeltproject.org/api/v2/context/context?format=html&timespan=15H&query=india&mode=artlist&maxrecords=75&format=json&sort=DateDesc#' > res.json")          
#%%
def APIResp(text):
    url = 'http://localhost:5002/auto_labeller'
    body = {}
    body['text'] = text
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(body), headers=headers,verify=False)
    resp = r.json()
    what = r.status_code
    return resp

#connecting with the database.
db = sqlite3.connect("testing.db")
#db.execute("drop table if exists results")
try:
    db.execute("create table results(id int PRIMARY KEY,url text, Date datetime, title text,seendate text,socialimage text, domain text, language text, isquote text, sentence text, context text, label text)")
except:
    print("table already found")
def savetoDB(url, title, seendate, socialimage, domain, language, isquote, sentence, context, label):
    #inserting values inside the created table
    db = sqlite3.connect("testing.db")
    from datetime import date
    Date = date.today().strftime("%d-%m-%Y")
    cmd = "insert into results(url, title, seendate, socialimage, domain, language, isquote, sentence, context, label) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(url, title, seendate, socialimage, domain, language, isquote, sentence, context, label)
    db.execute(cmd)
    db.commit()

def query():
    db = sqlite3.connect("testing.db")
    qry = "SELECT * FROM results"
    df = pd.read_sql_query(qry, db)
    df.head()
    return df

def db2CSV():
    db = sqlite3.connect("testing.db")
    qry = "SELECT * FROM results"
    df = pd.read_sql_query(qry, db)
    df.to_csv("DB.csv")
    return "CSV file uddated with name DB.csv"
#%%
with open("res.json", "r+") as temp:
    data = json.load(temp)
    if len(data["articles"])!=0:
        cols = list(data["articles"][0].keys())
        for r in range(0, len(data["articles"])):
            keys = list(data["articles"][r].keys())
            vals = list(data["articles"][r].values())
            label = APIResp(data["articles"][r]["context"])
            try:
                resp = label["res"][0]
                vals.append(resp)
            except:
                vals.append("NoLabel")
            for i in range(0, len(vals)):
                vals[i] = str(vals[i]).replace("'","-")
            savetoDB(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],str(vals[6]),str(vals[7]),vals[8],vals[9])
#%%
db2CSV()