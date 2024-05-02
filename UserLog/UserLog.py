import csv
import sqlite3
import sys
from datetime import datetime


def main(log_file, users_file):
    log_data = []
    users_data = []
    with open(log_file, encoding='koi8_r') as fin:
        for i in csv.reader(fin):
            j = []
            for k in i:
                 j.append(k.encode('koi8_r').decode('utf-8'))
            if j[0] != "#error":
                j[0] = j[0].split("_")[-1]
                j[1] = j[1][1:]
                if datetime.strptime(j[1], '%Y-%m-%d %H:%M:%S'):
                    if j[1][13] != ":":
                        j[1] = j[1][:11] + '0' + j[1][11:]
                    log_data.append(j)
    with open(users_file, encoding='koi8_r') as fin:
        for i in csv.reader(fin):
            j = i[0].split("\t")
            if j[0][:5] == "User_":
                if j[0][5:].isdigit():
                    j[0] = j[0][5:]
                    users_data.append(j)                
    log_data.sort()
    users_data.sort()
    with sqlite3.connect('users_log.s3db') as conn:
        cur = conn.cursor()
        for user_id, time, bet, win in log_data:
          cur.execute('INSERT INTO LOG (user_id, time, bet, win) VALUES (?, ?, ?, ?)',(user_id, time, bet, win))       
        for user_id, email, geo in users_data:
          cur.execute('INSERT INTO USERS (user_id, email, geo) VALUES ((SELECT user_id FROM LOG WHERE user_id = ?), ?, ?)',(user_id, email, geo))  
        conn.commit()



if name =='main':
  main(sys.argv[1], sys.argv[2])
