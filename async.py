import time
import os

while True:
    os.system("curl 'https://api.gdeltproject.org/api/v2/context/context?format=html&timespan=15H&query=india&mode=artlist&maxrecords=75&format=json&sort=DateDesc#' > res.json")          
    print("Asynchronous job : Runs once per an hour ")
    time.sleep(3600)
