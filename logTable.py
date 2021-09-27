import sqlite3
from datetime import datetime
import threading
from time import sleep
# from wiringthread import mytable
lock = threading.Lock()

sqlite_file = '/home/pi/Desktop/simple_flask/ToData.db'
conn = sqlite3.connect(sqlite_file, check_same_thread=False)




def create_table():

    # lock start
    lock.acquire()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS DATA(id INTEGER PRIMARY KEY,kinds INT, date DATE,time DATETIME, mode INT, message TEXT , duration FLOAT )"  )     

    cur.close()
    # lock close
    lock.release()

def create_table():
    # lock start
    lock.acquire()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS SYSTEM(FTPTIME DATETIME)")
       
    cur.close()
    # lock close
    lock.release()

    

def insert_table1(FTPTIME):
    # lock start
    lock.acquire()
    cur = conn.cursor()
    cur.execute("INSERT INTO SYSTEM (FTPTIME ) VALUES (?)",
                (FTPTIME,))

    conn.commit()
    cur.close()

    # lock close
    lock.release()
    return cur.lastrowid
    
    



def insert_table(kinds, date,time, mode, message, duration=0):
    # lock start
    lock.acquire()

    cur = conn.cursor()
    cur.execute("INSERT INTO DATA(kinds, date, time, mode, message, duration) VALUES (?, ?, ?, ?, ?,?)",
                (kinds, date, time, mode, message, duration))

    conn.commit()
    cur.close()
    # lock close

    lock.release()
    return cur.lastrowid
    
    

def one_day():

    # lock start
    lock.acquire()
    cur = conn.cursor()
    cur.execute("select kinds, date, count(date) from DATA WHERE mode = 1 group by date, kinds order by date DESC ,kinds")

    # lock close
    lock.release()
    return cur.fetchall()
    


def one_hour(date, gender):

    # lock start
    lock.acquire()
    cur = conn.cursor()
    cur.execute("select strftime('%H:00:00', time),"
                " count(strftime('%H', time)) from DATA where mode = 1 AND date =? AND kinds=? "
                "group by strftime('%H', time) order by kinds",
                (date, gender,))
    # lock close
    lock.release()

    return cur.fetchall()
    



def average_one_day(gender):

    # lock start
    lock.acquire()

    cur = conn.cursor()
    cur.execute("select date,avg(duration),"
                "count(date) from DATA where mode =1  AND kinds = ?"
                "group by date order by date DESC, kinds",
                (gender,))

    # lock close
    lock.release()

    return cur.fetchall()
    


def average_one_hour(date,gender):

   # lock start
    lock.acquire()

    cur = conn.cursor()
    cur.execute("select strftime('%H:00:00',time),avg(duration),"
                "count(strftime('%H',time)) from DATA where mode = 1 AND date = ? AND kinds = ?"
                "group by strftime('%H',time) order by kinds",
                (date, gender,))
    
    # lock close
    lock.release()
    
    return cur.fetchall()
    


def update_table(user_id, duration):

    # lock start
    lock.acquire()

    cur = conn.cursor()
    cur.execute("UPDATE DATA SET duration = ? WHERE id=?", (duration, user_id))
    conn.commit()
    cur.close()
    # lock close
    lock.release()

def update_table1(FTP):

    # lock start
    lock.acquire()

    cur = conn.cursor()
    cur.execute("UPDATE SYSTEM SET FTP = ? ",(FTP))
    conn.commit()
    cur.close()
   # lock close
    lock.release()
#
#print(average_one_day())