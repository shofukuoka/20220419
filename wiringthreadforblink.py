# coding: UTF -8
import wiringpi as wiringpi
from time import sleep
from datetime import datetime, timedelta
import time
import threading
import pygame.mixer
#from pygame.mixer import Sound
import logTable
import json




logTable.create_table()

pygame.mixer.init()
#pygame.mixer.pre_init(44100,-16,2, 1024)
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer =512)



with open('/home/pi/Desktop/simple_flask/config.json') as f:
    config = json.load(f)
GPIO_LED = config["GPIO_LED1"]
GPIO_SW = config["GPIO_SW1"]

#GPIO_LED = 12
#GPIO_SW = 26

wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(GPIO_LED, 1)  # sets GPIO 12 to output
wiringpi.pinMode(GPIO_SW, 0)  # sets GPIO 26 to input
wiringpi.pullUpDnControl(GPIO_SW, wiringpi.PUD_DOWN)

wiringpi.digitalWrite(GPIO_LED, 0)  # sets port 26 to 0 (0V, on)

log_file = "/home/pi/Desktop/simple_flask/LOG/log.txt"
error_log = "/home/pi/Desktop/simple_flask/LOG/error_log.txt"
status_log = "/home/pi/Desktop/simple_flask/LOG/status_log.txt"

global counter
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
counter5 = 0
user_id = 0
status_blink = False

def blink_led():
    while True: # Run forever
        wiringpi.digitalWrite(GPIO_LED, 0) # Turn on
        sleep(0.5) # Sleep for 1 second
        wiringpi.digitalWrite(GPIO_LED, 1) # Turn off
        sleep(0.5)
        global stop_threads 
        if stop_threads: 
            break
stop_threads = False
start_blink = threading.Thread(target=blink_led, args=())
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




def thAnn1():
    global  counter1
    global user_id
    counter1 += 1
    print ("男子 duration : 1  minutes",counter1)
    store_log(str(counter1))
    sound0 = pygame.mixer.Sound("/home/pi/Desktop/simple_flask/announce/announce1.wav")
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(2.0, 0.0)
    #logTable.update_table(user_id,1.0)




def thAnn2():
    global  counter2
    global user_id
    counter2 += 1
    print ("男子 duration : 2 minutes", counter2)
    store_log(str(counter2))
    sound0 = pygame.mixer.Sound("/home/pi/Desktop/simple_flask/announce/announce2.wav")
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(2.0, 0.0)
    #logTable.update_table(user_id, 2.0)


def thAnn3():
    global counter3
    global user_id
    counter3 += 1
    print ("男子 duration : 3  minutes" , counter3)
    store_log(str(counter3))
    sound0 = pygame.mixer.Sound("/home/pi/Desktop/simple_flask/announce/announce3.wav")
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(2.0, 0.0)
    #logTable.update_table(user_id, 3.0)
    start_blink.start()


def thAnn4():
    global counter4
    global user_id
    counter4 += 1
    print ("男子 duration : 4  minutes", counter4)
    store_log(str(counter4))
    sound0 = pygame.mixer.Sound("/home/pi/Desktop/simple_flask/announce/announce4.wav")
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(2.0, 0.0)
    #logTable.update_table(user_id, 4.0)


def thAnn5():
    global counter5
    global user_id
    counter5 += 1
    print ("男子 duration : 5  minutes", counter5)
    sound0 = pygame.mixer.Sound("/home/pi/Desktop/simple_flask/announce/announce4.wav")
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0, 10)
    channel0.set_volume(2.0, 0.0)




def stop_thAnn5():
    th5.cancel()

th1 = threading.Timer(60, thAnn1)
th2 = threading.Timer(120, thAnn2)
th3 = threading.Timer(180, thAnn3)
th4 = threading.Timer(240, thAnn4)
th5 = threading.Timer(300, thAnn5)

def start_waiting():
    global th1
    global th2
    global th3
    global th4
    global th5

    th1 = threading.Timer(60, thAnn1)
    th2 = threading.Timer(120, thAnn2)
    th3 = threading.Timer(180, thAnn3)
    th4 = threading.Timer(240, thAnn4)
    th5 = threading.Timer(300, thAnn5)


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
    durationStop = datetime.now() - timedelta(days=1)
    duration1 = 0
    start_d = datetime.now()
    global user_id
    global start
    global end
    global status_blink
    global stop_threads

    start_time = 0
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
#        date_time = now.strftime("[%Y/%m/%d  %H:%M:%S]")
        current_date= now.strftime("%Y:%m:%d")
        current_time = now.strftime("%H:%M:%S")
        end = datetime.now()
        
        #        print "read0= %d" % read0
        if status_blink:
            if (datetime.now() - durationStop).seconds>5:
                stop_threads = True
                start_blink.join()
                status_blink = False

        if read1 == read2:
            if read1 == 1:
                duration1 = datetime.now() - durationStop
                print (duration1)
                if duration1.seconds < 5 :
                    thAnn5()
                    start_d = datetime.now()
                    wiringpi.digitalWrite(GPIO_LED, 0) # switch on LED. Sets port 12 to 1 (3V3, on)
                    # status("Busy")
                    # print ("\n Boybusy")
                    # store_log(str(logcount) + "男子 トイレ使用開始\n")
                    user_id = logTable.insert_table(1, current_date, current_time , 0, "Boy Busy", duration = duration)

                else:
                    stop_thAnn5()
                    logcount = logcount + 1
                    start_d = datetime.now()
                    start_waiting()
                    print ("person count:" + str(logcount))
                    wiringpi.digitalWrite(GPIO_LED, 0)  # switch on LED. Sets port 12 to 1 (3V3, on)
                    store_log(str(logcount) + "男子 トイレ使用開始\n")
                    status("Busy")
                    print("\n Boybusy")
                    user_id = logTable.insert_table(1, current_date, current_time, 1, "Boy Busy", duration=duration)




            else:
                stop_waiting()
                durationStop = datetime.now()
                time_end = datetime.now()
                duration = time_end - start_d
                duration = duration.seconds/60.0
                wiringpi.digitalWrite(GPIO_LED, 1) # switch off LED. Sets port 12 to 0 (0V, off)
                pygame.mixer.Channel(0).stop()
                store_log("男子トイレ使用終了\n")
                user_id = logTable.insert_table(1, current_date, current_time, 2, "Boy Free", duration=duration)
                status("Free")
                print (duration)
                print ("\n男子トイレ使用終了")

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




