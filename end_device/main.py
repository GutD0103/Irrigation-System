import time
import threading
import json
import random
from scheduler import Scheduler
from mqtt import MyMQTTClient
from rs485 import RS485Communication
from datetime import datetime

AIO_USERNAME = "GutD"
AIO_KEY = ""
AIO_FEED_ID = ["irrigation","task","log","sensor"]


mqtt_client = MyMQTTClient(AIO_USERNAME, AIO_KEY, AIO_FEED_ID)
rs485 = RS485Communication(baudrate=9600, timeout=1)

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

class Sensor:
    def __init__(self) -> None:
        self.humi = 0
        self.temp = 0


    def to_dict(self):
        return {
            'humi': self.humi,
            'temp': self.temp,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def __str__(self):
        return self.to_json()
    
def myProcessMess(feed_id, payload):
    if feed_id == "irrigation":
        print(payload)
        mess.append(payload)

soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
soil_humidity = [1, 3, 0, 7, 0, 1, 53, 203]

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
flag_send = 0
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
start_time_send = 0
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


def publish_state():
    if myprogress.mixer1_percent > 100:
        myprogress.mixer1_percent = 100
    if myprogress.mixer2_percent > 100:
        myprogress.mixer2_percent = 100
    if myprogress.mixer3_percent > 100:
        myprogress.mixer3_percent = 100
    if myprogress.pumpout > 100:
        myprogress.pumpout = 100
    print(str(myprogress))
    mqtt_client.publish_data("task",str(myprogress))

def checking_send_success(start_time_send, value):
    if(time.time() - start_time_send > 1):
        print("TIMEOUT")
        return -1
    if(rs485.buffer.is_available()):
        value_t = value[:6]
        data = rs485.buffer.pop()
        data_array = [b for b in data]
        data_t = data_array[:6]
        print(data_t)
        print(value_t)
        if value_t == data_t:
            return 1
        return -1
    
    return 0

def irrigation():
    global state 
    global flag 
    global flag_send
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
    global start_time_send
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
            duration = (duration.total_seconds()) 

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
            flag_send = 1
    elif(state == STATE_MIXER_1):
        if(mixer1 != 0):
            if flag_send:
                rs485.send_data(mixer1_ON)
                start_time_send = time.time()
                flag_send = 0
                return
            
            if not flag_send:
                return_v = checking_send_success(start_time_send,mixer1_ON)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
                
            print(f"MIXER 1 START IN {mixer1}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer1*10 , PERIOD = 0)
            start_time_sys = time.time()
            myprogress.current_task = "mixer1"
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), f"{myprogress.label}:Mixer 1 starts operating")
            state = STATE_WAIT_FOR_MIXER_1
        else:
            state = STATE_MIXER_2


    elif (state == STATE_WAIT_FOR_MIXER_1):

        if(flag):
            if flag_send:
                rs485.send_data(mixer1_OFF)
                start_time_send = time.time()
                flag_send = 0
                return
            
            if not flag_send:
                return_v = checking_send_success(start_time_send,mixer1_OFF)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
            
            print("MIXER 1 STOP")
            flag = 0
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), f"{myprogress.label}:Mixer 1 stops operating")
            state = STATE_MIXER_2

        myprogress.mixer1_percent = round(((time.time() - start_time_sys) / mixer1) * 100)

    elif (state == STATE_MIXER_2):


        if(mixer2 != 0):
            if flag_send:
                rs485.send_data(mixer2_ON)
                start_time_send = time.time()
                flag_send = 0
                return
            
            if not flag_send:
                return_v = checking_send_success(start_time_send,mixer2_ON)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
        
            print(f"MIXER 2 START IN {mixer2}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer2*10 , PERIOD = 0)
            start_time_sys = time.time()
            myprogress.current_task = "mixer2"
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), f"{myprogress.label}:Mixer 2 starts operating")
            state = STATE_WAIT_FOR_MIXER_2
        else:
            state = STATE_MIXER_3


    elif (state == STATE_WAIT_FOR_MIXER_2):


        if(flag):
            if flag_send:
                rs485.send_data(mixer2_OFF)
                start_time_send = time.time()
                flag_send = 0
                return
            
            if not flag_send:
                return_v = checking_send_success(start_time_send,mixer2_OFF)
                if return_v== -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v== 0: # not getting response
                    return
                
            print("MIXER 2 STOP")
            flag = 0
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), f"{myprogress.label}:Mixer 2 stops operating")
            state = STATE_MIXER_3

        myprogress.mixer2_percent = round(((time.time() - start_time_sys) / mixer2) * 100)

    elif (state == STATE_MIXER_3):


        if(mixer3 != 0):
            if flag_send:
                rs485.send_data(mixer3_ON)
                start_time_send = time.time()
                flag_send = 0
                return
            
            if not flag_send:
                return_v = checking_send_success(start_time_send,mixer3_ON)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
                
            print(f"MIXER 3 START IN {mixer3}")
            scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = mixer3*10 , PERIOD = 0)
            start_time_sys = time.time()
            myprogress.current_task = "mixer3"
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), f"{myprogress.label}:Mixer 3 starts operating")
            state = STATE_WAIT_FOR_MIXER_3
        else:
            state = STATE_PUMP_IN


    elif (state == STATE_WAIT_FOR_MIXER_3):


        if(flag):
            if flag_send:
                rs485.send_data(mixer3_OFF)
                start_time_send = time.time()
                flag_send = 0
                return
            
            if not flag_send:
                return_v = checking_send_success(start_time_send,mixer3_OFF)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
                
            print("MIXER 3 STOP")
            flag = 0
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), f"{myprogress.label}:Mixer 3 stops operating")
            state = STATE_PUMP_IN

        myprogress.mixer3_percent = round(((time.time() - start_time_sys) / mixer3)*100)

    elif (state == STATE_PUMP_IN):
        if flag_send:
            rs485.send_data(pumpin_ON)
            start_time_send = time.time()
            flag_send = 0
            return
        if not flag_send:
            return_v = checking_send_success(start_time_send,pumpin_ON)
            if return_v == -1: #send fail
                flag_send = 1
                return
            elif return_v == 1: #send success
                flag_send = 1
            elif return_v == 0: # not getting response
                return
            
        print("PUMP IN START")
        scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = 100 , PERIOD = 0)
        state = STATE_WAIT_FOR_PUMP_IN


    elif (state == STATE_WAIT_FOR_PUMP_IN):


        if(flag):
            if flag_send:
                rs485.send_data(pumpin_OFF)
                start_time_send = time.time()
                flag_send = 0
                return
            if not flag_send:
                return_v = checking_send_success(start_time_send,pumpin_OFF)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
                
            print("PUMP IN STOP")
            flag = 0
            state = STATE_SELECTED


    elif (state == STATE_SELECTED):
        

        if(area1 > 0):
            if flag_send:
                rs485.send_data(area1_ON)
                start_time_send = time.time()
                flag_send = 0
                return
            if not flag_send:
                return_v = checking_send_success(start_time_send,area1_ON)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
            
            print("SELECT AREA 1")
            area1 = -1

        if(area2 > 0):
            if flag_send:
                rs485.send_data(area2_ON)
                start_time_send = time.time()
                flag_send = 0
                return
            if not flag_send:
                return_v = checking_send_success(start_time_send,area2_ON)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
            print("SELECT AREA 2")
            area2 = -1

        if(area3 > 0):
            if flag_send:
                rs485.send_data(area3_ON)
                start_time_send = time.time()
                flag_send = 0
                return
            if not flag_send:
                return_v = checking_send_success(start_time_send,area3_ON)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
            print("SELECT AREA 3")
            area3 = -1
        
        
        if flag_send:
            rs485.send_data(pumpout_ON)
            start_time_send = time.time()
            flag_send = 0
            return
        if not flag_send:
            return_v = checking_send_success(start_time_send,pumpout_ON)
            if return_v == -1: #send fail
                flag_send = 1
                return
            elif return_v == 1: #send success
                flag_send = 1
            elif return_v == 0: # not getting response
                return
        print(f"PUMP OUT START IN {duration}")
        publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), f"{myprogress.label}:Start watering")
        start_time_sys = time.time()
        myprogress.current_task = "pump out"
        state = STATE_PUMP_OUT
        scheduler.SCH_Add_Task(pFunction = set_flag, DELAY = duration*10 , PERIOD = 0)


    elif (state == STATE_PUMP_OUT):

        myprogress.pumpout  = round(((time.time() - start_time_sys) / (duration)) * 100)

        if(flag):
            if area1 == -1:
                if flag_send:
                    rs485.send_data(area1_OFF)
                    start_time_send = time.time()
                    flag_send = 0
                    return
                if not flag_send:
                    return_v = checking_send_success(start_time_send,area1_OFF)
                    if return_v == -1: #send fail
                        flag_send = 1
                        return
                    elif return_v == 1: #send success
                        flag_send = 1
                    elif return_v == 0: # not getting response
                        return
                area1 = 1
                print("STOP SELECT AREA 1")


            if area2 == -1:
                if flag_send:
                    rs485.send_data(area2_OFF)
                    start_time_send = time.time()
                    flag_send = 0
                    return
                if not flag_send:
                    return_v = checking_send_success(start_time_send,area2_OFF)
                    if return_v == -1: #send fail
                        flag_send = 1
                        return
                    elif return_v == 1: #send success
                        flag_send = 1
                    elif return_v == 0: # not getting response
                        return
                area2 = 1
                print("STOP SELECT AREA 2")

            if area3 == -1:
                if flag_send:
                    rs485.send_data(area3_OFF)
                    start_time_send = time.time()
                    flag_send = 0
                    return
                if not flag_send:
                    return_v = checking_send_success(start_time_send,area3_OFF)
                    if return_v == -1: #send fail
                        flag_send = 1
                        return
                    elif return_v == 1: #send success
                        flag_send = 1
                    elif return_v == 0: # not getting response
                        return
                area3 = 1
                print("STOP SELECT AREA 3")


            if flag_send:
                rs485.send_data(pumpout_OFF)
                start_time_send = time.time()
                flag_send = 0
                return
            if not flag_send:
                return_v = checking_send_success(start_time_send,pumpout_OFF)
                if return_v == -1: #send fail
                    flag_send = 1
                    return
                elif return_v == 1: #send success
                    flag_send = 1
                elif return_v == 0: # not getting response
                    return
                
            
            publish_log(datetime.now().strftime("%d/%m/%Y %H:%M"), f"{myprogress.label}:Stop watering")
            print("PUMP OUT STOP")
            mycycle += 1
            flag = 0
            state = STATE_IDLE

INIT = 0
READ_DATA = 1
PUBLISH_DATA = 2
sensor_state = INIT
sensor_data = Sensor()
flag_sensor = 0

def set_flag_sensor():
    global flag_sensor
    flag_sensor = 1

def crc16_modbus(data: list) -> list:
    crc = 0xFFFF  # Khởi tạo CRC với giá trị 0xFFFF
    for pos in data:
        crc ^= pos  # XOR byte hiện tại với CRC
        for _ in range(8):  # Xử lý từng bit trong byte
            if crc & 1:  # Nếu bit ít quan trọng nhất (LSB) là 1
                crc >>= 1  # Dịch phải CRC một bit
                crc ^= 0xA001  # XOR với đa thức 0xA001
            else:  # Nếu LSB là 0
                crc >>= 1  # Dịch phải CRC một bit
    
    crc_low = crc & 0xFF  # Byte thấp
    crc_high = (crc >> 8) & 0xFF  # Byte cao
    
    return [crc_low, crc_high]  # Trả về mảng chứa byte thấp và byte cao

def read_data_sensor():
    global sensor_state
    global state
    global flag_sensor
    global sensor_data
    if(sensor_state == INIT):
        scheduler.SCH_Add_Task(pFunction = set_flag_sensor, DELAY = 5*10 , PERIOD = 0)
        sensor_state = READ_DATA
    elif(sensor_state == READ_DATA):
        if(flag_sensor):
            flag_sensor = 0
            if(state == STATE_IDLE):
                # rs485.send_data(soil_humidity)
                # rs485.send_data(soil_temperature)
                print("send data")
                sensor_state = PUBLISH_DATA
            scheduler.SCH_Add_Task(pFunction = set_flag_sensor, DELAY = 2*10 , PERIOD = 0)

    elif(sensor_state == PUBLISH_DATA):
        
        # if rs485.buffer.is_available():
        #     print("read data")
        #     data = rs485.buffer.pop()
        #     data_array = [b for b in data]
        #     print(data_array)
        #     crc = data_array[-2:]
        #     payload_array = data_array[:6]

        #     if crc != crc16_modbus(payload_array):
        #         return
            
        #     if(data_array[:4] == soil_humidity[:4]):
        #         sensor_data.humi  = data_array[rs485.buffer.size_of_object - 4] * 256 + data_array[rs485.buffer.size_of_object - 3]
        #     if(data_array[:4] == soil_temperature[:4]):
        #         sensor_data.temp  = data_array[rs485.buffer.size_of_object - 4] * 256 + data_array[rs485.buffer.size_of_object - 3]
            

        if(flag_sensor):
            flag_sensor = 0
            if sensor_data.temp == 0  or sensor_data.humi == 0:
                sensor_data.temp = random.randint(30, 40)
                sensor_data.humi = random.randint(70, 100)
                mqtt_client.publish_data("sensor",str(sensor_data))
            else:
                sensor_data.temp = random.randint(30, 40)
                sensor_data.humi = random.randint(70, 100)
                mqtt_client.publish_data("sensor",str(sensor_data))

            scheduler.SCH_Add_Task(pFunction = set_flag_sensor, DELAY = 30*10 , PERIOD = 0)
            sensor_state = READ_DATA



def main():

    # serial init
    # rs485.processData = myProcessData
    mqtt_client.processMessage = myProcessMess
    #mqtt init
    mqtt_client.start()

    scheduler.SCH_Add_Task(pFunction = publish_state, DELAY = 5*10 , PERIOD = 7.5*10)


    while True:
        scheduler.SCH_Update()
        scheduler.SCH_Dispatch_Tasks()
        rs485.read_serial()
        irrigation()
        read_data_sensor()
        time.sleep(0.1)
    
if __name__ == "__main__":
    start_time = time.time()
    main()
