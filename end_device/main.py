import time
import threading
import json
from scheduler import Scheduler
from mqtt import MyMQTTClient
from rs485 import RS485Communication
from datetime import datetime

AIO_USERNAME = "GutD"
AIO_KEY = "aio_TNaU20Pmw9L7x41vHH4ifs3ZKSit"
AIO_FEED_ID = ["irrigation","task","log"]


mqtt_client = MyMQTTClient(AIO_USERNAME, AIO_KEY, AIO_FEED_ID)
rs485 = None
# rs485 = RS485Communication(baudrate=115200, timeout=1)

mess = []

class Progress:
    def __init__(self) -> None:
        self.id = None
        self.label = None
        self.current_task = ""
        self.mixer1_percent = 0
        self.mixer2_percent = 0
        self.mixer3_percent = 0
        self.pumpout = 0

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'current_task': self.current_task,
            'mixer1_percent': self.mixer1_percent,
            'mixer2_percent': self.mixer2_percent,
            'mixer3_percent': self.mixer3_percent,
            'pumpout': self.pumpout,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def __str__(self):
        return self.to_json()
    
class Log:
    def __init__(self) -> None:
        self.time = None
        self.mess = None


    def to_dict(self):
        return {
            'time': self.time,
            'mess': self.mess,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def __str__(self):
        return self.to_json()
    
def myProcessMess(feed_id, payload):
    if feed_id == "irrigation":
        print(payload)
        mess.append(payload)

def myProcessData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[0] == "TEMP":
        mqtt_client.publish_data("temperature",splitData[1])
    elif splitData[0] == "LUX":
        mqtt_client.publish_data("lux",splitData[1])
    elif splitData[0] == "HUMI":
        mqtt_client.publish_data("humidity",splitData[1])
    else:
        print("we dont have that measurement to publish")
    pass

pumpin_ON       = [0x07, 0x06, 0x00, 0x00, 0x00, 0xFF, 0xC9, 0xEC]
pumpin_OFF      = [0x07, 0x06, 0x00, 0x00, 0x00, 0x00, 0x89, 0xAC]
pumpout_ON      = [0x08, 0x06, 0x00, 0x00, 0x00, 0xFF, 0xC9, 0x13]
pumpout_OFF     = [0x08, 0x06, 0x00, 0x00, 0x00, 0x00, 0x89, 0x53]
mixer1_ON       = [0x01, 0x06, 0x00, 0x00, 0x00, 0xFF, 0xC9, 0x8A]
mixer1_OFF      = [0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x89, 0xCA]
mixer2_ON       = [0x02, 0x06, 0x00, 0x00, 0x00, 0xFF, 0XC9, 0xB9] 
mixer2_OFF      = [0x02, 0x06, 0x00, 0x00, 0x00, 0x00, 0x89, 0xF9] 
mixer3_ON       = [0x03, 0x06, 0x00, 0x00, 0x00, 0xFF, 0xC8, 0x68] 
mixer3_OFF      = [0x03, 0x06, 0x00, 0x00, 0x00, 0x00, 0x88, 0x28]
area1_ON        = [0x04, 0x06, 0x00, 0x00, 0x00, 0xFF, 0xC9, 0xDF]
area1_OFF       = [0x04, 0x06, 0x00, 0x00, 0x00, 0x00, 0x89, 0x9F]
area2_ON        = [0x05, 0x06, 0x00, 0x00, 0x00, 0xFF, 0xC8, 0x0E]
area2_OFF       = [0x05, 0x06, 0x00, 0x00, 0x00, 0x00, 0x88, 0x4E]
area3_ON        = [0x06, 0x06, 0x00, 0x00, 0x00, 0xFF, 0xC8, 0x3D]
area3_OFF       = [0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x88, 0x7D]

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
start_time_sys = time.time()
mycycle = 0

mylog = Log()
myprogress = Progress()

def set_flag():
    global flag
    flag = 1 

def publish_log(time, mess):
    global mylog
    mylog.time = time
    mylog.mess = mess
    mqtt_client.publish_data("log",str(mylog))

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
    global start_time_sys
    global myprogress
    

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
            duration = (duration.total_seconds()) * 10

            start_time_sys = time.time()
            print(f"Process {data}")
            state = STATE_MIXER_1

            myprogress.id = data["id"]
            myprogress.label = data["label"]

            if(mixer1 == 0):
                myprogress.mixer1_percent = -1
            else:
                myprogress.mixer1_percent = 0

            if(mixer2 == 0):
                myprogress.mixer2_percent = -1
            else:
                myprogress.mixer2_percent = 0

            if(mixer3 == 0):
                myprogress.mixer3_percent = -1
            else:
                myprogress.mixer3_percent = 0

            myprogress.pumpout = 0
                 
    elif(state == STATE_MIXER_1):
        if(mixer1 != 0):
            # rs485.send_data(mixer1_ON)
            print(f"MIXER 1 START IN {mixer1}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer1*10 , PERIOD = 0)
            start_time_sys = time.time()
            myprogress.current_task = "mixer1"
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), "Mixer 1 starts operating")
            state = STATE_WAIT_FOR_MIXER_1
        else:
            state = STATE_MIXER_2


    elif (state == STATE_WAIT_FOR_MIXER_1):
        

        if(flag):
            # rs485.send_data(mixer1_OFF)
            print("MIXER 1 STOP")
            flag = 0
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), "Mixer 1 stops operating")
            state = STATE_MIXER_2

        myprogress.mixer1_percent = round(((time.time() - start_time_sys) / mixer1) * 100)

    elif (state == STATE_MIXER_2):


        if(mixer2 != 0):
            # rs485.send_data(mixer2_ON)
            print(f"MIXER 2 START IN {mixer2}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer2*10 , PERIOD = 0)
            start_time_sys = time.time()
            myprogress.current_task = "mixer2"
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), "Mixer 2 starts operating")
            state = STATE_WAIT_FOR_MIXER_2
        else:
            state = STATE_MIXER_3


    elif (state == STATE_WAIT_FOR_MIXER_2):


        if(flag):
            print("MIXER 2 STOP")
            # rs485.send_data(mixer2_OFF)
            flag = 0
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), "Mixer 2 stops operating")
            state = STATE_MIXER_3

        myprogress.mixer2_percent = round(((time.time() - start_time_sys) / mixer2) * 100)

    elif (state == STATE_MIXER_3):


        if(mixer3 != 0):
            # rs485.send_data(mixer3_ON)
            print(f"MIXER 3 START IN {mixer3}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer3*10 , PERIOD = 0)
            start_time_sys = time.time()
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), "Mixer 3 starts operating")
            myprogress.current_task = "mixer3"
            state = STATE_WAIT_FOR_MIXER_3
        else:
            state = STATE_PUMP_IN


    elif (state == STATE_WAIT_FOR_MIXER_3):


        if(flag):
            # rs485.send_data(mixer3_OFF)
            print("MIXER 3 STOP")
            flag = 0
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), "Mixer 3 stops operating")
            state = STATE_PUMP_IN

        myprogress.mixer3_percent = round(((time.time() - start_time_sys) / mixer3)*100)

    elif (state == STATE_PUMP_IN):
        # rs485.send_data(pumpin_ON)
        print("PUMP IN START")
        scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = 100 , PERIOD = 0)
        state = STATE_WAIT_FOR_PUMP_IN


    elif (state == STATE_WAIT_FOR_PUMP_IN):


        if(flag):
            # rs485.send_data(pumpin_OFF)
            print("PUMP IN STOP")
            flag = 0
            state = STATE_SELECTED


    elif (state == STATE_SELECTED):
        

        if(area1):
            # rs485.send_data(area1_ON)
            print("SELECT AREA 1")
            pass
        if(area2):
            # rs485.send_data(area2_ON)
            print("SELECT AREA 2")
            pass
        if(area3):
            # rs485.send_data(area3_ON)
            print("SELECT AREA 3")
            pass
        
        print(f"PUMP OUT START IN {duration}")
        # rs485.send_data(pumpout_ON)
        start_time_sys = time.time()
        publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), "Start watering")
        myprogress.current_task = "pump out"
        state = STATE_PUMP_OUT
        scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = duration , PERIOD = 0)


    elif (state == STATE_PUMP_OUT):

        myprogress.pumpout  = round(((time.time() - start_time_sys) / (duration / 10)) * 100)

        if(flag):
            # rs485.send_data(area1_OFF)
            # rs485.send_data(area2_OFF)
            # rs485.send_data(area3_OFF)
            # rs485.send_data(pumpout_OFF)
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), "Stop watering")
            print("PUMP OUT STOP")
            mycycle += 1
            flag = 0
            state = STATE_IDLE

def publish_state():
    print(str(myprogress))
    mqtt_client.publish_data("task",str(myprogress))

def main():

    # serial init
    # rs485.processData = myProcessData
    mqtt_client.processMessage = myProcessMess
    #mqtt init
    mqtt_client.start()

    scheduler.SCH_Add_Task(pFunction = publish_state, DELAY = 5*10 , PERIOD = 10*10)


    while True:
        scheduler.SCH_Update()
        scheduler.SCH_Dispatch_Tasks()
        irrigation()
        time.sleep(0.1)
    
if __name__ == "__main__":
    start_time = time.time()
    main()
