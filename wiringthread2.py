# coding: UTF -8
import wiringpi as wiringpi
from time import sleep
from datetime import datetime,timedelta
import time
import threading
#import pygame
#from signal import pause
import logTable
import commentjson
import pygame.mixer


#pygame.mixer.quit()

logTable.create_table()

pygame.mixer.init()
#pygame.mixer.pre_init(44100,-16,2, 1024)
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer =512)
#pygame.mixer.stop()

with open('/home/pi/Desktop/simple_flask/config.json') as f:
    config = commentjson.load(f)
GPIO_LED = config["GPIO_LED2"] #GPIO LED=24
GPIO_SW = config["GPIO_SW2"]   #GPIO SW=5

announce1 = config["Gannounce1"]
announce2 = config["Gannounce2"]
announce3 = config["Gannounce3"]
announce4 = config["Gannounce4"]

t1 = config["Gthannounce1"]
t2 = config["Gthannounce2"]
t3 = config["Gthannounce3"]
t4 = config["Gthannounce4"]
t5 = config["Gthannounce5"]

door2opentime = config["Door2opentime"]
blinktime2 = config["Blinktime2"]


wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(GPIO_LED, 1)  # sets GPIO 24 to output
wiringpi.pinMode(GPIO_SW, 0)  # sets GPIO 5 to input
wiringpi.pullUpDnControl(GPIO_SW, wiringpi.PUD_DOWN)

wiringpi.digitalWrite(GPIO_LED, 0)  # sets port 24 to 0 (0V, on)

log2_file = "/home/pi/Desktop/simple_flask/LOG/log2.txt"
error2_log = "/home/pi/Desktop/simple_flask/LOG/error2_log.txt"
status2_log = "/home/pi/Desktop/simple_flask/LOG/status2_log.txt"

start2_blink = None

global counter
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
counter5 = 0
user_id = 0
status2_blink = False

def blink_led():
    while True:
        wiringpi.digitalWrite(GPIO_LED,1)
        sleep(0.5)
        wiringpi.digitalWrite(GPIO_LED,0)
        sleep(0.5)
        global stop2_threads
        if stop2_threads:
            break
stop2_threads = False

def count2_people():
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d")
    f = open(log2_file, "r", )
    data1 = f.read().split("\n")
    f.close()
    temp2 = 0
    for x in data1:
        if date_time in x:
            temp2 = temp2 + 1

    return temp2




def thAnn1():
    global counter1
    global user_id
    #print("debug 1min")
    counter1 += 1
    print ("女子 duration : 1  minutes", counter1)
    sound1 = pygame.mixer.Sound(announce1)
    channel1 = pygame.mixer.Channel(1)
    channel1.play(sound1)
    channel1.set_volume(0.0, 2.0)
    #logTable.update_table(user_id, 1.0)



def thAnn2():
    global counter2
    global user_id
    #print("debug 2min")
    counter2 += 1
    print ("女子 duration : 2  minutes", counter2)
    sound1 = pygame.mixer.Sound(announce2)
    channel1 = pygame.mixer.Channel(1)
    channel1.play(sound1)
    channel1.set_volume(0.0, 2.0)
    #logTable.update_table(user_id, 2.0)


def thAnn3():
    global counter3
    global user_id
    counter3 += 1
    #print("debug 3min")
    print ("女子 duration : 3  minutes", counter3)
    sound1 = pygame.mixer.Sound(announce3)
    channel1 = pygame.mixer.Channel(1)
    channel1.play(sound1)
    channel1.set_volume(0.0, 2.0)



def thAnn4():
    global counter4
    global user_id
    #print("debug 4min")
    counter4 += 1
    print ("女子 duration : 4  minutes", counter4)
    sound1 = pygame.mixer.Sound(announce4)
    channel1 = pygame.mixer.Channel(1)
    channel1.play(sound1)
    channel1.set_volume(0.0, 2.0)



def thAnn5():
    global counter5
    global user_id
    #print("debug 5min")
    counter5 += 1
    print ("女子 duration : 5  minutes", counter5)
    sound1 = pygame.mixer.Sound(announce4)
    channel1 = pygame.mixer.Channel(1)
    channel1.play(sound1,10)
    channel1.set_volume(0.0, 2.0)




def stop_thAnn5():
    th5.cancel()



th1 = threading.Timer(t1, thAnn1)
th2 = threading.Timer(t2, thAnn2)
th3 = threading.Timer(t3, thAnn3)
th4 = threading.Timer(t4, thAnn4)
th5 = threading.Timer(t5, thAnn5)


def start_waiting():
    global th1
    global th2
    global th3
    global th4
    global th5

    th1 = threading.Timer(t1, thAnn1)
    th2 = threading.Timer(t2, thAnn2)
    th3 = threading.Timer(t3, thAnn3)
    th4 = threading.Timer(t4, thAnn4)
    th5 = threading.Timer(t5, thAnn5)

    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()


def stop_waiting():
    th1.cancel()
    th2.cancel()
    th3.cancel()
    th4.cancel()
    th5.cancel()

    

def start():
    global counter
    global user_id
    global start
    global end 
    global status2_blink
    global start2_blink
    global stop2_threads
    
    durationStop2 = datetime.now() - timedelta(days = 1)
    duration2 = 0
    status2_toilet = "free"
    start_d = datetime.now()
    start_time = datetime.now()
    read0 = 1
    log2count = count2_people()
    temp2_count = log2count

    while True:
        time.sleep(0.1)
        read1 = wiringpi.digitalRead(GPIO_SW)
        #        print "read1= %d" % read1
        #print("debug girl blink check\n ")
        if status2_blink and (status2_toilet == "free"):
            #print("debug girl blink stop")
            if (datetime.now() - durationStop2).seconds > 1:
                try:
                    print("\n girl stop blink")
                    #print("stop blink")
                    stop2_threads = True
                    start2_blink.join()
                    status2_blink = False
                    duration = (datetime.now() - start_time).seconds /60  #For 1 min
                    start_time = datetime.now()
                    duration =str(duration)
                    store2_log(duration + "\n 男子トイレ使用終了\n")
                    status2("free")
                    print (duration)
                    
                    temp2_count = log2count
                    status2_toilet = "free"
                except:
                    print("girl stop blink err ")
        
        elif (not status2_blink) and status2_toilet == "busy":
            #print("debug girl blink start\n")
            if(datetime.now() - start_time).seconds > blinktime2 :
                try:
                    stop2_threads = False
                    print("girl start blink")
                    start2_blink = threading.Thread(target = blink_led, args = ())
                    start2_blink.start()
                    status2_blink = True
                except:
                    print("girl start blink err")
        if read0 == read1:

            continue

        time.sleep(0.05)
        read2 = wiringpi.digitalRead(GPIO_SW)
        now = datetime.now()
        current = datetime.now()
        current_date = now.strftime("%Y/%m/%d ")
        current_time = now.strftime("%H:%M:%S")
        end = datetime.now()

        #        print "read0= %d" % read0
        if read1 == read2:
            if read1 == 1:
                
                duration2 = datetime.now() - durationStop2
                start_waiting()
    #            print(duration2)
                
                if (duration2.seconds) < door2opentime:
                    #thAnn5()
                    #start_d = datetime.now()
                    #print("debug girl within 5sec")
                    try:
                        status2_toilet = "busy"
                        wiringpi.digitalWrite(GPIO_LED, 1) # switch on LED. Sets port 18 to 1 (3V3, on)
                        user_id = logTable.insert_table(2, current_date, current_time,3, "Girl ON/Off", duration = 0)
                        status2("\ngirl on/off\n")
                        print ("\n girl on/off")
                    except:
                        print("girl on/off err")
                
                else:
                    #print("debug girl busy")
                #    stop_thAnn5()
                    try:
                        start_time = datetime.now()
                        status2_toilet = "busy"
                        #print("debug after girl ")
                        log2count = log2count + 1
                        #print("debug girl after logcount ")
                        start_d = datetime.now()
                        print ("person count:" + str(log2count))
                        #print("debug girl after print log count")
                        
                        wiringpi.digitalWrite(GPIO_LED, 1) 
                        #print("debug girl after gpio led show ") # switch on LED. Sets port 18 to 1 (3V3, on)
                        store2_log(str(log2count) + "女子 トイレBusy\n")
                        #print("debug girl after log store")
                        status2("Girl Busy")
                        print ("\n Girl Busy\n")
                        #print("debug before insert girl to db")
                        user_id = logTable.insert_table(2, current_date, current_time, 1, "Girl Busy", duration=0)
                        #print("debug after girl log inserted to db")
                    except:
                        print("girl busy err ")    

            else:
                try:
                    #print("debug girl ann stop")
                    stop_waiting()
                    #print("debug girl after stop th")
                    status2_toilet = "free"
                    durationStop2 = datetime.now()
                    time_end = datetime.now()
                    duration = time_end - start_d
                    #duration = duration.seconds/60.0
                    #print("debug girl before gpio stop")
                    wiringpi.digitalWrite(GPIO_LED, 0) # switch off LED. Sets port 18 to 0 (0V, off)
                    #print("debug girl before stop ann")
                    pygame.mixer.Channel(1).stop()
                    #print("debug girl after stop ann")
                    duration = str(duration)
                #    store2_log("女子 トイレFree\n")
                    store2_log(duration + "\n 女子トイレ使用終了\n")
                    #print("debug girl before insert db for stop")
                    user_id = logTable.insert_table(2,current_date, current_time, 2, "Girl Free", duration= duration)
                    #print("debug girl after insert db for stop")
                    print("\n Girl Free")
                    #print (duration)
                    status2("Free")
                    temp2_count = log2count
                #   print ("\n女子トイレFree\n")
                except:
                    print("girl off err ")
                if temp2_count > log2count:
                    logTable.update_table(user_id , duration)
                    temp2_count = log2count


        read0 = read1



def store2_log(log):
    global log2count
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d  %H:%M:%S]")
    text_log2 = date_time + " " + log
    try:
        f = open(log2_file, "a+")
        f = f.write(text_log2)
        f.close()
    except:
        store_error2("file open error!!\n")


def status2(log):
    #   print(log)
    try:
        f = open(status2_log, "w+")
        f.write(log)
        f.close()
    except:
        store_error2("file open error!!\n")


def store_error2(log):
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d  %H:%M:%S]")
    text_log = date_time + " " + log
    try:
        f = open(error2_log, "a+")
        f.write(text_log)
        f.close()
    except:
        print("ERROR")