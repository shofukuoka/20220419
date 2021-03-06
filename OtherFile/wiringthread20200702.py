# coding: UTF -8
import wiringpi as wiringpi
from time import sleep
from datetime import datetime
import time
import threading
import pygame.mixer
#from pygame.mixer import Sound
import logTable
import ctypes


logTable.create_table()
pygame.mixer.init(frequency=44800, size=-16, channels=2, buffer =614)

GPIO_LED = 12
GPIO_SW = 26

wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(GPIO_LED, 1)  # sets GPIO 12 to output
wiringpi.pinMode(GPIO_SW, 0)  # sets GPIO 26 to input
wiringpi.pullUpDnControl(GPIO_SW, wiringpi.PUD_DOWN)

wiringpi.digitalWrite(GPIO_LED, 0)  # sets port 26 to 0 (0V, on)

log_file = "./LOG/log.txt"
error_log = "./LOG/error_log.txt"
status_log = "./LOG/status_log.txt"

global counter
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
user_id = 0

def count_people():
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d")
    f = open(log_file, "r", )
    data = f.read().split("\n")
    f.close()
    temp = 0
    for x in data:
        if date_time in x:
            temp = temp + 1

    return temp


def aa():
    global  counter1
    global user_id

    counter1 += 1
    print ("男子 duration : 1  minutes",counter1)
    store_log(str(counter1))
    sound0 = pygame.mixer.Sound('/home/pi/Desktop/simple_flask/announce/announce1.wav')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(1.0, 0.0)
#    logTable.update_table(user_id,3)




def bb():
    global  counter2
    global user_id
    global duration
    counter2 += 1
    print "男子 duration : 2 minutes", counter2
    store_log(str(counter2))
    sound0 = pygame.mixer.Sound('/home/pi/Desktop/simple_flask/announce/announce2.wav')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(1.0, 0.0)
#    logTable.update_table(user_id, 6)


def cc():
    global counter3
    global user_id
    global duration
    counter3 += 1
    print "男子 duration : 3  minutes" , counter3
    store_log(str(counter3))
    sound0 = pygame.mixer.Sound('/home/pi/Desktop/simple_flask/announce/announce3.wav')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(1.0, 0.0)
#    logTable.update_table(user_id, 9)


def dd():
    global counter4
    global user_id
    global duration
    counter4 += 1
    print "男子 duration : 4  minutes", counter4
    store_log(str(counter4))
    sound0 = pygame.mixer.Sound('/home/pi/Desktop/simple_flask/announce/announce4.wav')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(1.0, 0.0)
#    logTable.update_table(user_id, 12)


t = threading.Timer(60, aa)
t1 = threading.Timer(120, bb)
t2 = threading.Timer(180, cc)
t3 = threading.Timer(240, dd)
def start_waiting():
    global t
    global t1
    global t2
    global t3
    t = threading.Timer(60, aa)
    t1 = threading.Timer(120, bb)
    t2 = threading.Timer(180, cc)
    t3 = threading.Timer(240, dd)

    t.start()
    t1.start()
    t2.start()
    t3.start()

def stop_waiting():

    t.cancel()
    t1.cancel()
    t2.cancel()
    t3.cancel()

def start():
    global counter
    global user_id
    time_start = 0
    read0 = 1
    logcount = count_people()
    while True:

        time.sleep(0.1)
        read1 = wiringpi.digitalRead(GPIO_SW)
        #        print "read1= %d" % read1
        if read0 == read1:
            continue

        time.sleep(0.05)
        read2 = wiringpi.digitalRead(GPIO_SW)
        now = datetime.now()
        current_date= now.strftime("%Y:%m:%d")
        current_time = now.strftime("%H:%M:%S")
        end = datetime.now()
        
        #        print "read0= %d" % read0
        if read1 == read2:
            if read1 == 1:

                logcount = logcount + 1
                print "person count:" +str(logcount)
                time_start = time.monotonic()
                print now
                print("男子トイレ使用開始\n")
                start_waiting()
                wiringpi.digitalWrite(GPIO_LED, 0) # switch on LED. Sets port 12 to 1 (3V3, on)
                store_log(str(logcount) + "男子 トイレ使用開始\n" )
                status("Busy")

                user_id = logTable.insert_table(1, current_date, current_time , 1, "Boy Busy", duration)


            else:
                stop_waiting()
                time_end = time.monotonic()
                duration = time_end - time_start
                wiringpi.digitalWrite(GPIO_LED, 1) # switch off LED. Sets port 12 to 0 (0V, off)
                pygame.mixer.Channel(0).stop()
                store_log("男子トイレ使用終了\n")
                user_id = logTable.insert_table(1, current_date, current_time, 2, "Boy Free", duration)
                status("Free")
                print "\n男子トイレ使用終了"
                print end
                

        read0 = read1


def store_log(log):
    global logcount
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d  %H:%M:%S]")
    text_log = date_time + " " + log
    try:
        f = open(log_file, "a+", )
        f = f.write(text_log)
        f.close()
    except:
        store_error("file open error!!\n")



def status(log):
    #   print(log)
    try:
        f = open(status_log, "w+")
        f.write(log)
        f.close()
    except:
        store_error("file open error!!\n")


def store_error(log):
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d  %H:%M:%S]")
    text_log = date_time + " " + log
    try:
        f = open(error_log, "a+")
        f.write(text_log)
        f.close()
    except:
        print("ERROR")



x= threading.Thread(target = start)
x.start()


