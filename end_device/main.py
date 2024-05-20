import time
import threading
import json
from scheduler import Scheduler
from mqtt import MyMQTTClient
from rs485 import RS485Communication
from datetime import datetime

AIO_USERNAME = "GutD"
AIO_KEY = "aio_Nwzq32rUpNpxj5bhqcus2DSRu7Hb"
AIO_FEED_ID = ["irrigation"]


mqtt_client = MyMQTTClient(AIO_USERNAME, AIO_KEY, AIO_FEED_ID)
rs485 = RS485Communication(baudrate=115200, timeout=1)

mess = []

def myProcessMess(feed_id, payload):
    if feed_id == "irrigation":
        print(payload)
        mess.append(payload)

def myProcessData():
    pass

pumpin_ON       = [0, 6, 0, 0, 0, 255, 200, 91]
pumpin_OFF      = [0, 6, 0, 0, 0, 0, 136, 27]
pumpout_ON      = [0, 6, 0, 0, 0, 255, 200, 91]
pumpout_OFF     = [0, 6, 0, 0, 0, 255, 200, 91]
mixer1_ON       = [0, 6, 0, 0, 0, 255, 200, 91]
mixer1_OFF      = [0, 6, 0, 0, 0, 255, 200, 91]
mixer2_ON       = [0, 6, 0, 0, 0, 255, 200, 91]
mixer2_OFF      = [0, 6, 0, 0, 0, 255, 200, 91]
mixer3_ON       = [0, 6, 0, 0, 0, 255, 200, 91]
mixer3_OFF      = [0, 6, 0, 0, 0, 255, 200, 91]
area1_ON        = [0, 6, 0, 0, 0, 255, 200, 91]
area1_OFF       = [0, 6, 0, 0, 0, 255, 200, 91]
area2_ON        = [0, 6, 0, 0, 0, 255, 200, 91]
area2_OFF       = [0, 6, 0, 0, 0, 255, 200, 91]
area3_ON        = [0, 6, 0, 0, 0, 255, 200, 91]
area3_OFF       = [0, 6, 0, 0, 0, 255, 200, 91]

scheduler_main = Scheduler()
scheduler = Scheduler()

STATE_IDLE=                 10
STATE_MIXER_1 =             0
STATE_WAIT_FOR_MIXER_1 =    1
STATE_MIXER_2 =             2
STATE_WAIT_FOR_MIXER_2 =    3
STATE_MIXER_3 =             4
STATE_WAIT_FOR_MIXER_3 =    5
STATE_PUMP_IN =             6
STATE_WAIT_FOR_PUMP_IN =    7
STATE_SELECTED =            8
STATE_PUMP_OUT =            9

state = STATE_IDLE
flag = 0
mixer1 = 100
mixer2 = 100
mixer3 = 100
area1 = 1
area2 = 1
area3 = 0
duration = 0
cycle = 0

mycycle = 0

def set_flag():
    global flag
    flag = 1 

def irrigation():
    global state 
    global flag 
    global mixer1 
    global mixer2 
    global mixer3 
    global area1 
    global area2
    global area3 
    global cycle 
    global mycycle
    global duration
    if(state == STATE_IDLE):

        if(len(mess) > 0 ):
            tem_mess = mess.pop(0)
            data = json.loads(tem_mess)
            mixer1 = data["mixer"][0]
            mixer2 = data["mixer"][1]
            mixer3 = data["mixer"][2]

            areas = data["area"]
            area1 = 1 if "1" in areas else 0
            area2 = 2 if "2" in areas else 0
            area3 = 3 if "3" in areas else 0

            start_time_str = data["start_time"]
            end_time_str = data["end_time"]
            start_time = datetime.strptime(start_time_str, "%H:%M")
            end_time = datetime.strptime(end_time_str, "%H:%M")
            duration = end_time - start_time
            duration = (duration.total_seconds() / 60) * 10

            print(f"Process {data}")
            state = STATE_MIXER_1

    elif(state == STATE_MIXER_1):

        if(mixer1 != 0):
            print(f"MIXER 1 START IN {mixer1}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer1 , PERIOD = 0)
            state = STATE_WAIT_FOR_MIXER_1
        else:
            state = STATE_MIXER_2


    elif (state == STATE_WAIT_FOR_MIXER_1):


        if(flag):
            print("MIXER 1 STOP")
            flag = 0
            state = STATE_MIXER_2


    elif (state == STATE_MIXER_2):


        if(mixer2 != 0):
            print(f"MIXER 2 START IN {mixer2}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer2 , PERIOD = 0)
            state = STATE_WAIT_FOR_MIXER_2
        else:
            state = STATE_MIXER_3


    elif (state == STATE_WAIT_FOR_MIXER_2):


        if(flag):
            print("MIXER 2 STOP")
            flag = 0
            state = STATE_MIXER_3


    elif (state == STATE_MIXER_3):


        if(mixer3 != 0):
            print(f"MIXER 3 START IN {mixer3}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer3 , PERIOD = 0)
            state = STATE_WAIT_FOR_MIXER_3
        else:
            state = STATE_PUMP_IN


    elif (state == STATE_WAIT_FOR_MIXER_3):


        if(flag):
            print("MIXER 3 STOP")
            flag = 0
            state = STATE_PUMP_IN


    elif (state == STATE_PUMP_IN):

        print("PUMP IN START")
        scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = 100 , PERIOD = 0)
        state = STATE_WAIT_FOR_PUMP_IN


    elif (state == STATE_WAIT_FOR_PUMP_IN):


        if(flag):
            
            print("PUMP IN STOP")
            flag = 0
            state = STATE_SELECTED


    elif (state == STATE_SELECTED):
        

        if(area1):
            print("SELECT AREA 1")
            pass
        if(area2):
            print("SELECT AREA 2")
            pass
        if(area3):
            print("SELECT AREA 3")
            pass
        
        print(f"PUMP OUT START IN {duration}")
        state = STATE_PUMP_OUT
        scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = duration , PERIOD = 0)


    elif (state == STATE_PUMP_OUT):

        if(flag):
            print("PUMP OUT STOP")
            mycycle += 1
            flag = 0
            state = STATE_IDLE






def main():

    # serial init
    rs485.processData = myProcessData
    mqtt_client.processMessage = myProcessMess
    #mqtt init
    mqtt_client.start()


    while True:
        scheduler.SCH_Update()
        scheduler.SCH_Dispatch_Tasks()
        irrigation()
        time.sleep(0.1)
    
if __name__ == "__main__":
    main()
