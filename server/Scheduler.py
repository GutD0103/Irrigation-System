from datetime import datetime, time, timedelta
from database import TaskDatabase
import signal
from TaskInfor import TaskInformation
from mqtt import MyMQTTClient
import threading
import schedule
import json
import inspect
import re
import os
import time
import copy
import sys

class Scheduler:
    def __init__(self,Database,DataTable, AIO_user, AIO_key,AIO_feed):
        self.__Start_Schedule = schedule.Scheduler()
        self.__task_db = TaskDatabase(db_name=Database,table_name=DataTable)
        self.ListTask = []
        self.FlagOUT = 0
        self.FlagSetStreamKey = 0
        self.CurrentTask = None
        self.ListTask = []

        AIO_USERNAME = AIO_user
        AIO_KEY = AIO_key
        self.AIO_FEED_ID = AIO_feed

        self.mqtt_client = MyMQTTClient(AIO_USERNAME, AIO_KEY, self.AIO_FEED_ID)

        self.mqtt_client.start()
        self.mutex = threading.Lock()

    def write_flag(self,value):
        self.mutex.acquire()
        self.FlagOUT = value
        self.mutex.release()

    def is_out(self):
        out = 0
        self.mutex.acquire()
        out = self.FlagOUT
        self.mutex.release()

        return out

    def __removeTask_byid(self,target_id):
        index_to_remove = None
        for i, task_info in enumerate(self.ListTask):
            if task_info.ID == target_id:
                index_to_remove = i
                break
            
        if index_to_remove is not None:
            del self.ListTask[index_to_remove]
            print(f"Deleted at index {target_id}")

            with open(self.FileLog, 'r') as file:
                lines = file.readlines()
            del lines[index_to_remove]
            with open(self.FileLog, "w") as f:
                for line in lines:
                    f.write(line)
            return True
        else:
            print(f"Cannot find ID {target_id}")
            return False
        
    def __removeTask_bylabel(self,label):
        indices_to_remove = [] 
        for i, task_info in enumerate(self.ListTask):
            if task_info.label == label:
                indices_to_remove.append(i)

        if len(indices_to_remove) == 0:
            return False
        
        for index in reversed(indices_to_remove):
            del self.ListTask[index]

        return True
    

    
    def __task(self,taskinfor):

        self.mqtt_client.publish_data(self.AIO_FEED_ID,json.dumps(taskinfor.to_json()))

        self.CurrentTask = taskinfor

    def __weekly_task(self,taskinfor):
        days_mapping = {
            'mon': self.__Start_Schedule.every().monday,
            'tue': self.__Start_Schedule.every().tuesday,
            'wed': self.__Start_Schedule.every().wednesday,
            'thu': self.__Start_Schedule.every().thursday,
            'fri': self.__Start_Schedule.every().friday,
            'sat': self.__Start_Schedule.every().saturday,
            'sun': self.__Start_Schedule.every().sunday
        }
        print("WEEKLY TASK")
        print(taskinfor.days)
        for day in taskinfor.days:
            if day in days_mapping:
                days_mapping[day.lower()].at(taskinfor.start_time).until(taskinfor.until).do(self.__task,taskinfor).tag(f'{taskinfor.ID}',f'{taskinfor.label}')

    def weekly_task(self,taskinfor):
        # TO DO
        new_ID = self.__task_db.add_task(taskinfor)
        taskinfor.ID = new_ID
        self.ListTask.append(taskinfor)
        self.__weekly_task(taskinfor)
        print(self.__Start_Schedule.get_jobs())


    def __daily_task(self,taskinfor):

        self.mqtt_client.publish_data(self.AIO_FEED_ID,json.dumps(taskinfor.to_json()))
        self.CurrentTask = taskinfor
    


    def daily_task(self,taskinfor):
        new_ID = self.__task_db.add_task(taskinfor)
        taskinfor.ID = new_ID
        self.ListTask.append(taskinfor)
        self.__Start_Schedule.every().days.at(taskinfor.start_time).until(taskinfor.until).do(self.__daily_task, taskinfor).tag(f'{taskinfor.ID}',f'{taskinfor.label}')
        print(self.__Start_Schedule.get_jobs())


    def __onetime_task(self,taskinfor):
        print("ONE TIME")
        self.mqtt_client.publish_data(self.AIO_FEED_ID,json.dumps(taskinfor.to_json()))
        self.CurrentTask = taskinfor
        return schedule.CancelJob
    
    def onetime_task(self,taskinfor):
        new_ID = self.__task_db.add_task(taskinfor)
        taskinfor.ID = new_ID
        self.ListTask.append(taskinfor)
        self.__Start_Schedule.every().days.at(taskinfor.start_time).do(self.__onetime_task,taskinfor).tag(f'{taskinfor.ID}',f'{taskinfor.label}')
        print(self.__Start_Schedule.get_jobs())

    
    def delete_task(self,id = 0, label = 0):
        flag = 0
        if id == "all":
            self.__Start_Schedule.clear()
            self.__task_db.delete_all_tasks()
            self.ListTask.clear()
            print(schedule.get_jobs())
            return True
        elif id:
            if self.__removeTask_byid(int(id)):
                self.__task_db.delete_task(ID=id)
                self.__Start_Schedule.clear(id)
                print(self.__Start_Schedule.get_jobs())
                flag = 1

        if label:
            if self.__removeTask_bylabel(label=label):
                self.__task_db.delete_task(label=label)
                self.__Start_Schedule.clear(label)
                print(self.__Start_Schedule.get_jobs())
                flag = 1

        return flag
        
    def __job(self):
        print("#######################################")
        print('Start SCHEDULER')
        print(self.__Start_Schedule.get_jobs())
        print('Stop SCHEDULER')
        print("#######################################")


    def get_current_task(self):
        return self.CurrentTask

    def get_schedule(self):
        return self.ListTask
    
    def __run(self):
        while not self.is_out():
            self.__Start_Schedule.run_pending()
            time.sleep(1)
        sys.exit()
        print("OUT")

    def signal_handler(self, sig, frame):
        self.write_flag(1)
        print('You pressed Ctrl+C!')
        

    def run(self):
        # INIT MQTT
        # self.__Stop_Schedule.every(10).seconds.do(self.__job)
        signal.signal(signal.SIGINT, self.signal_handler)
        schedule_thread = threading.Thread(target=self.__run)
        schedule_thread.start()



    

if __name__ == "__main__":
    pass
