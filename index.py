import requests
import json
from datetime import datetime
import time
import csv
import sqlite3

lasttimestamp = int(0)
balance = 0.00000000001

db = sqlite3.connect('data.db')
cursor = db.cursor()

while True:
    x = 2
    time.sleep(300)
    
    req = requests.get('https://api.ethermine.org/miner/d97bf35716037d654789549d72beAF3926D4DeAb/dashboard').json()

    for i in req["data"]['workers']:
        timestamp = i['lastSeen']
        name = str(i['worker'])
        hashrate = int(i['currentHashrate'])
        #print(name, timestamp, hashrate)
        print(name, timestamp)

        userexist = cursor.execute(f'SELECT EXISTS(SELECT 1 FROM users WHERE name="{name}");')
        userexist = str(cursor.fetchall())

        if "0" in userexist:
            db.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (name, timestamp, hashrate, balance))
            db.commit()
            pass
        else:
            db.execute('UPDATE users SET hashrate = ? WHERE name = ?', 
            (hashrate, str(name)))
            db.commit()
            pass

        lasttimestamp = db.execute('SELECT lasthashrate FROM users WHERE name = ?', (name,)).fetchall()
        lasttimestamp = str(lasttimestamp)
        bad_chars = ['[', '(', ',', "]", ")"]
        for i in bad_chars :
            lasttimestamp = lasttimestamp.replace(i, "")
        lasttimestamp = int(lasttimestamp)
        print(name, lasttimestamp)

        if timestamp != lasttimestamp:
            revenu = ((hashrate/1000000)*0.056)*0.0208333
            actualbalance = db.execute('SELECT balance FROM users WHERE name = ?', (name,)).fetchall()
            actualbalance = str(actualbalance)
            bad_chars = ['[', '(', ',', "]", ")"]
            for i in bad_chars :
                actualbalance = actualbalance.replace(i, "")
            actualbalance = float(actualbalance)
            db.execute('UPDATE users SET balance = ? WHERE name = ?', 
            (float(revenu)+actualbalance, str(name)))
            db.commit()
            #print(revenu)
            time.sleep(1)
            db.execute('UPDATE users SET lasthashrate = ? WHERE name = ?', 
            (int(timestamp), str(name)))
            db.commit()
            pass
        else:
            db.execute('UPDATE users SET lasthashrate = ? WHERE name = ?', 
            (int(timestamp), str(name)))
            db.commit()
            pass