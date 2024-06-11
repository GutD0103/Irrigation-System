# API Documentation

## Overview
This API provides endpoints for managing tasks related to irrigation system

## Install


## Run the app

    python Server.py

# REST API FOR SCHEDULER

The REST API to the example app is described below.

## Get Schedule
Retrieves the schedule of tasks.

### Request

`GET /get/schedule`

    localhost:5000//get/schedule

### Response
Success: Returns a JSON object containing the schedule details.

        {
            "Schedule": [
            {
                "ID": 8,
                "label": "TEST",
                "mixer": [0,50,50],
                "area": ["1","2","3"],
                "duration": 0,
                "start_date": "2024-04-12",
                "until": "2024-04-12",
                "start_time": "10:00",
                "end_time": "13:00",
                "typetask": "onetime",
                "days": []
                }
            ]
        }

## Get Current Task
Retrieves information about the current task.
### Request

`GET /get/currentTask`

    localhost:5000//get/currentTask
### Response
Success: Returns a JSON object containing information about the current task.


## Add One Weekly Task.

Adds a one-time streaming task.

### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `duration` | optional, default: 1 | Interval in days between each live stream occurrence. |
| `starttime` | optional, default: current time | Start time of the task (format: HH:MM). |
| `endtime` | optional | End time of the task (format: HH:MM). |
| `startdate` | optional, default: current time | Start date of the task (format: YYYY-MM-DD). |
| `until` | optional | End date for the recurring task (optional, format: YYYY-MM-DD). |
| `label` | required| Name of this task. |
| `days` | required, value: ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]| Names of the days of the week. |
| `mixer1` |required| Amount of solution for mixer1 |
| `mixer2` |required| Amount of solution for mixer2  |
| `mixer3` |required| Amount of solution for mixer3  |
| `area` |required| Areas|

### Request

`GET /schedule/addTask/weekly`

    localhost:5000//schedule/addTask/weekly?starttime=10:00&endtime=13:00&startdate=2024-04-12&until=2024-04-15&label=TEST&days=mon,tue&mixer1=50&mixer2=50&mixer3=50&area=1,2,3

### Response
Success: Returns a success message along with the ID of the created task.
    
    "success": {
       "message": "Create task",
       "ID": 3
     }
## Add Daily Task.

Adds a daily recurring streaming task.

### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `duration` | optional, default: 1 | Interval in days between each live stream occurrence. |
| `starttime` | optional, default: current time | Start time of the task (format: HH:MM). |
| `endtime` | optional | End time of the task (format: HH:MM). |
| `startdate` | optional, default: current time | Start date of the task (format: YYYY-MM-DD). |
| `until` | optional | End date for the recurring task (optional, format: YYYY-MM-DD). |
| `label` | required| Name of this task. |
| `mixer1` |required| Amount of solution for mixer1 |
| `mixer2` |required| Amount of solution for mixer2  |
| `mixer3` |required| Amount of solution for mixer3  |
| `area` |required| Areas|
### Request

`GET /schedule/addTask/daily`

    localhost:5000//schedule/addTask/daily?starttime=10:00&endtime=13:00&startdate=2024-04-12&until=2024-04-15&label=TEST&mixer1=50&mixer2=50&mixer3=50&area=1,2,3

### Response
Success: Returns a success message along with the ID of the created task.
    
    "success": {
       "message": "Create task",
       "ID": 1
     }

## Add One Time Task.

Adds a one-time streaming task.

### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `starttime` | optional, default: current time | Start time of the task (format: HH:MM). |
| `endtime` | optional | End time of the task (format: HH:MM). |
| `startdate` | optional, default: current time | Start date of the task (format: YYYY-MM-DD). |
| `label` |required| Name of this task. |
| `mixer1` |required| Amount of solution for mixer1 |
| `mixer2` |required| Amount of solution for mixer2  |
| `mixer3` |required| Amount of solution for mixer3  |
| `area` |required| Areas|

### Request

`GET /schedule/addTask/onetime`

    localhost:5000//schedule/addTask/onetime?starttime=10:00&endtime=13:00&startdate=2024-04-12&label=TEST&mixer1=50&mixer2=50&mixer3=50&area=1,2,3

### Response
Success: Returns a success message along with the ID of the created task.
    
    "success": {
       "message": "Create task",
       "ID": 2
     }

## Delete Task

Deletes a task by ID.

### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `id` | optional | ID of the task to delete, or "all" to delete all tasks. |
| `label` | optional| Name of this task. |

* This request requires at least 1 parameter.
### Request

`GET /schedule/deleteTask`

    localhost:5000//schedule/deleteTask?id=1&label=TEST

### Response
Success: Returns a success message along with the ID of the created task.
    
    "success": {
       "message": "Delete task",
       "ID": 1
     }

