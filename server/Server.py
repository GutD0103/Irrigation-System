from flask import Flask, request, jsonify, abort
from datetime import datetime, time, timedelta

from database import TaskDatabase
from TaskInfor import TaskInformation
from Scheduler import Scheduler
import json
import re
import os
import time
import copy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

FolderVideoPath = "video"

ADAFRUIT_AIO_USERNAME = "GutD"
ADAFRUIT_AIO_KEY      = "aio_TNaU20Pmw9L7x41vHH4ifs3ZKSit"
feed = ["irrigation"]
my_scheduler = Scheduler(Database="schedule.db",DataTable="schedule",AIO_feed=feed,AIO_user=ADAFRUIT_AIO_USERNAME,AIO_key=ADAFRUIT_AIO_KEY)

################## begin MQTT



###################################################################################


def validateTimeformat(time_str):
    pattern = r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$'
    return re.match(pattern, time_str) is not None



################################################################################################################################################################

# @app.before_request
# def before_request_callback():
#     if request.method != 'GET':
#         abort(405)  # Trả về mã lỗi 405 Method Not Allowed cho các phương thức không phải GET trên tuyến đường nhất định

################################################################################################################################################################




@app.route('/get/currentTask')
def Get_Current_Task():

    if not my_scheduler.CurrentTask:
        return jsonify({'Current Task': "None"}), 200
    
    # Convert datetime objects to strings
    task = copy.deepcopy(my_scheduler.CurrentTask)
    if task:
        task.start_date = task.start_date.strftime("%Y-%m-%d")
        task.until = task.until.strftime("%Y-%m-%d") if task.until and task.until != "None" else None
        
    # Create dictionary
    task_dict = {"Current Task": task.__dict__}
    
    # Convert dictionary to JSON string
    json_string = json.dumps(task_dict, indent=4)
    
    return json_string


@app.route('/get/schedule')
def Get_schedule():
    # CHOOSE THE STREAM CHANEL

    # Convert datetime objects to strings
    mylist = copy.deepcopy(my_scheduler.ListTask)
    for task in mylist:
        task.start_date = task.start_date.strftime("%Y-%m-%d")
        task.until = task.until.strftime("%Y-%m-%d") if task.until and task.until != "None" else None

    # Create dictionary
    schedule_dict = {"Schedule": [task.__dict__ for task in mylist]}
    
    # Convert dictionary to JSON string
    json_string = json.dumps(schedule_dict, indent=4)

    return json_string


@app.route('/schedule/addTask/weekly',methods=['GET'])
def Add_Task_Everyweeks():
    start_time = request.args.get('starttime')
    end_time = request.args.get('endtime')
    start_date = request.args.get('startdate')
    mixer0 = request.args.get('mixer0')
    mixer1 = request.args.get('mixer1')
    mixer2 = request.args.get('mixer2')
    area = request.args.get('area') 
    duration = request.args.get('duration')
    until = request.args.get('until')
    label = request.args.get('label')
    days = request.args.get('days')

    deadline = None

    #CHECK DURATION
    print(duration)
    if not duration:
        int_duration = 1
        duration = 1
    elif duration.isdigit():
        int_duration = int(duration)
    else:
        return jsonify({'error':  'Wrong duration'}), 400
    
    #CHECK UNTIL
    if not until:
        my_year = 2100
        my_month = 12
        my_day = 12
        deadline = datetime(year=my_year,month=my_month,day=my_day,hour=23,minute=59,second=59)
    else:
        my_year = int(until.split('-')[0])
        my_month = int(until.split('-')[1])
        my_day = int(until.split('-')[2])
        deadline = datetime(year=my_year,month=my_month,day=my_day,hour=23,minute=59,second=59)
        if(deadline < datetime.now()):
            return jsonify({'error': 'until in the past'}), 400
    deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
    
    # CHECK START DATE
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            return jsonify({'error': 'Wrong start date format'}), 400
        
    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

    #CHECK START TIME
    if not start_time:
        now = datetime.now()
        start_time = now.strftime("%H:%M")
        print("Current Time =", start_time)
    else:
        if validateTimeformat(start_time) == False:
             return jsonify({'error': 'Wrong time format'}) ,400
        print(start_time)

    #CHECK END TIME
    if end_time:
        if validateTimeformat(start_time) == False:
             return jsonify({'error': 'Wrong time format'}) ,400
        print(end_time)
    else:
        return jsonify({'error': 'Empty end time'}) ,400
    
    if(datetime.strptime(end_time, "%H:%M") <= datetime.strptime(start_time, "%H:%M")):
        return jsonify({'error': 'Start time greater than end time'}) ,400
    
    # CHECK DAYS
    if not days:
        return jsonify({'error': 'Empty days'}) ,400
    else:
        days = days.split(',')
        list_days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        for day in days:
            if day not in list_days:
                return jsonify({'error': 'Wrong date'}) ,400

    #CHECK LABEL
    if not label:
        return jsonify({'error': 'Empty label'}) ,400

    
    # CHECK AREA

    if not area:
        return jsonify({'error': {'message': 'Area empty'}}), 400

    area = area.split(',')

    # CHECK MIXER
    if not mixer0:
        mixer0 = 0
    if not mixer1:
        mixer1 = 0
    if not mixer2:
        mixer2 = 0
    
    mixer = [int(mixer0),int(mixer1),int(mixer2)]

    new_task = TaskInformation(ID=None,label=label,days=days, area=area,mixer=mixer,start_date=start_date,duration=int(duration),until=deadline,start_time=start_time,end_time=end_time,typetask="weekly")
   
    my_scheduler.weekly_task(new_task)

    return jsonify({'success': {'message': 'Create task', 'ID': new_task.ID}}), 200

@app.route('/schedule/addTask/daily' , methods=['GET'])
def Add_Task_Everydays():
    if request.method == 'OPTIONS':
        return jsonify({'error':'Wrong stream'}), 400
    
    start_time = request.args.get('starttime')
    end_time = request.args.get('endtime')
    start_date = request.args.get('startdate')
    mixer0 = request.args.get('mixer0')
    mixer1 = request.args.get('mixer1')
    mixer2 = request.args.get('mixer2')
    area = request.args.get('area') 
    duration = request.args.get('duration')
    until = request.args.get('until')
    label = request.args.get('label')
    deadline = None


    print(duration)

    # CHECK DURATION 
    if not duration:
        int_duration = 1
        duration = 1
    elif duration.isdigit():
        int_duration = int(duration)
    else:
        return jsonify({'error':  'Wrong duration'}), 400
    
    #CHECK UNTIL
    if not until:
        my_year = 2100
        my_month = 12
        my_day = 12
        deadline = datetime(year=my_year,month=my_month,day=my_day,hour=23,minute=59,second=59)
    else:
        my_year = int(until.split('-')[0])
        my_month = int(until.split('-')[1])
        my_day = int(until.split('-')[2])
        deadline = datetime(year=my_year,month=my_month,day=my_day,hour=23,minute=59,second=59)
        if(deadline < datetime.now()):
            return jsonify({'error':  'until in the past'}), 400
        
    deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")

    # CHECK START DATE
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            return jsonify({'error': 'Wrong start date format'}), 400
        
    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
   # CHECK START TIME 
    if not start_time:
        now = datetime.now()
        start_time = now.strftime("%H:%M")
        print("Current Time =", start_time)
    else:
        if validateTimeformat(start_time) == False:
             return jsonify({'error': 'Wrong time format'}) ,400
        print(start_time)
    #CHECK END TIME
    if end_time:
        if validateTimeformat(start_time) == False:
             return jsonify({'error': 'Wrong time format'}) ,400
        print(end_time)
    else:
        return jsonify({'error': 'Empty end time'}) ,400
    
    if(datetime.strptime(end_time, "%H:%M") <= datetime.strptime(start_time, "%H:%M")):
        return jsonify({'error': 'Start time greater than end time'}) ,400
    
    #CHECK LABEL

    if not label:
        return jsonify({'error': 'Empty label'}) ,400

    
    # CHECK AREA

    if not area:
        return jsonify({'error': {'message': 'Area empty'}}), 400

    area = area.split(',')

    # CHECK MIXER
    if not mixer0:
        mixer0 = 0
    if not mixer1:
        mixer1 = 0
    if not mixer2:
        mixer2 = 0
    
    mixer = [int(mixer0),int(mixer1),int(mixer2)]

    #CREATE NEW TASK
    new_task = TaskInformation(ID=None,label=label,days = [],mixer=mixer,area=area,start_date=start_date,duration=int(duration),until=deadline,start_time=start_time,end_time=end_time,typetask="daily")
    my_scheduler.daily_task(new_task)

    return jsonify({'success': {'message': 'Create task', 'ID': new_task.ID}}), 200



@app.route('/schedule/addTask/onetime',methods=['GET'])
def Add_Task_onetime():
    start_time = request.args.get('starttime')
    end_time = request.args.get('endtime')
    start_date = request.args.get('startdate')
    label = request.args.get('label')
    mixer0 = request.args.get('mixer0')
    mixer1 = request.args.get('mixer1')
    mixer2 = request.args.get('mixer2')
    area = request.args.get('area') 
    until = None
  

    #CHECK START DATE
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    else:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
            
        except ValueError:
            return jsonify({'error':  'Wrong start date format'}), 400
    #CHECK START TIME
    if not start_time:
        now = datetime.now()
        start_time = now.strftime("%H:%M")
        print("Current Time =", start_time)
    else:

        if validateTimeformat(start_time) == False:
             return jsonify({'error': 'Wrong time format'}) ,400
        print(start_time)

    #CHECK END TIME
    if end_time:
        if validateTimeformat(start_time) == False:
             return jsonify({'error': 'Wrong time format'}) ,400
        print(end_time)
        str_end_time = datetime.strptime(end_time, "%H:%M")
    else:
        return jsonify({'error': 'Empty end time'}) ,400
    
    if(datetime.strptime(end_time, "%H:%M") <= datetime.strptime(start_time, "%H:%M")):
        return jsonify({'error': 'Start time greater than end time'}) ,400


    if str_end_time.time() <= datetime.strptime(start_time, "%H:%M").time():
        until = datetime.combine(start_date.date() + timedelta(days=1), str_end_time.time())
    else:
        until = datetime.combine(start_date.date(), str_end_time.time())

    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
    until = until.strftime("%Y-%m-%d %H:%M:%S")

    # CHECK LABLE

    if not label:
        return jsonify({'error': 'Empty label'}) ,400

    # CHECK AREA

    if not area:
        return jsonify({'error': {'message': 'Area empty'}}), 400

    area = area.split(',')

    # CHECK MIXER
    if not mixer0:
        mixer0 = 0
    if not mixer1:
        mixer1 = 0
    if not mixer2:
        mixer2 = 0
    
    mixer = [int(mixer0),int(mixer1),int(mixer2)]
    
    new_task = TaskInformation(ID=None,label=label,area=area,mixer=mixer,duration=0,start_date=start_date,until=until,start_time=start_time,end_time=end_time,typetask="onetime",days=[])
    my_scheduler.onetime_task(new_task)


    return jsonify({'success': {'message': 'Create task', 'ID': new_task.ID}}), 200


@app.route('/schedule/deleteTask')
def Delete_Task():
        # CHOOSE THE STREAM CHANEL
        
    id = request.args.get('id')
    label = request.args.get('label')
    print(id)
    if not id and not label:
        return jsonify({'error':  'ID and label empty'}), 400
    
    if not  my_scheduler.delete_task(id,label):
        return jsonify({'error':  'Cannot deleta'}), 400
    else:
        return jsonify({'success': {'message': 'Delete task', 'ID': f'{id}'}}), 200
    


def main():
    
    my_scheduler.run()

    # Running app
    app.run(debug=False)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        raise
        


