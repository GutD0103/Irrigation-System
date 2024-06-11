# API Documentation

## Overview
This API provides endpoints for managing tasks related to streaming, such as retrieving video files, setting stream keys, scheduling live streams, and managing scheduled tasks.

## Install


## Run the app

    python Server.py

# REST API FOR SCHEDULER

The REST API to the example app is described below.

## Get Schedule
Retrieves the schedule of streaming tasks.

### Request

`GET /get/schedule`

    localhost:5000//get/schedule

### Response
Success: Returns a JSON object containing the schedule details.

    {
        "Schedule": [
            {
            "ID": 1,
            "label": "VIPVCL",
            "video_name": [
            "ship.mp4"
            ],
            "duration": "2",
            "start_date": "2024-04-09 00:00:00",
            "until": "2024-04-16 00:00:00",
            "start_time": "10:49",
            "end_time": "13:00",
            "onetime": "0"
            },
            {
            "ID": 2,
            "label": "VIDEOLIST3",
            "video_name": [
            "ship.mp4"
            ],
            "duration": 2,
            "start_date": "2024-04-09 00:00:00",
            "until": "2024-04-16 23:59:59",
            "start_time": "10:49",
            "end_time": "13:00",
            "onetime": 0
            },
            {
            "ID": 3,
            "label": "VIDEOLIST2",
            "video_name": [
            "ship.mp4"
            ],
            "duration": 2,
            "start_date": "2024-04-09 00:00:00",
            "until": "2024-04-16 23:59:59",
            "start_time": "10:49",
            "end_time": "13:00",
            "onetime": 0
            }
        ]
    }

## Get Current Task
Retrieves information about the current task.
### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `stream` | required, defaul = 1 | Choose a streaming channel. |
### Request

`GET /get/currentTask`

    localhost:5000//get/currentTask?stream=1

### Response
Success: Returns a JSON object containing information about the current task.

    {
        "Current Task": {
            "ID": 4,
            "label": "VIDEOLIST2",
            "video_name": [
            "ship.mp4"
            ],
            "duration": 2,
            "start_date": "2024-04-09 00:00:00",
            "until": "2024-04-16 23:59:59",
            "start_time": "12:14",
            "end_time": "13:00",
            "onetime": 0
        }
    }


## Add One Weekly Task.

Adds a one-time streaming task.

### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `stream` | required, defaul = 1 | Choose a streaming channel. |
| `list` | required | Comma-separated list of video names. |
| `duration` | optional, default: 1 | Interval in days between each live stream occurrence. |
| `starttime` | optional, default: current time | Start time of the task (format: HH:MM). |
| `endtime` | optional | End time of the task (format: HH:MM). |
| `startdate` | optional, default: current time | Start date of the task (format: YYYY-MM-DD). |
| `until` | optional | End date for the recurring task (optional, format: YYYY-MM-DD). |
| `label` | required| Name of this task. |
| `days` | required, value: ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]| Names of the days of the week. |

### Request

`GET /schedule/addTask/weekly`

    localhost:5000//schedule/addTask/weekly?stream=1&list=bird.mp4&starttime=10:00&endtime=13:00&startdate=2024-04-12&until=2024-04-15&label=LISTVIDEO2&days=mon,tue

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
| `stream` | required, defaul = 1 | Choose a streaming channel. |
| `list` | required | Comma-separated list of video names. |
| `duration` | optional, default: 1 | Interval in days between each live stream occurrence. |
| `starttime` | optional, default: current time | Start time of the task (format: HH:MM). |
| `endtime` | optional | End time of the task (format: HH:MM). |
| `startdate` | optional, default: current time | Start date of the task (format: YYYY-MM-DD). |
| `until` | optional | End date for the recurring task (optional, format: YYYY-MM-DD). |
| `label` | required| Name of this task. |


### Request

`GET /schedule/addTask/daily`

    localhost:5000//schedule/addTask/daily?stream=1&list=bird.mp4&duration=2&starttime=10:00&endtime=13:00&startdate=2024-04-12&until=2024-04-15&label=LISTVIDEO1

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
| `stream` | required, defaul = 1 | Choose a streaming channel. |
| `list` | required | Comma-separated list of video names. |
| `starttime` | optional, default: current time | Start time of the task (format: HH:MM). |
| `endtime` | optional | End time of the task (format: HH:MM). |
| `startdate` | optional, default: current time | Start date of the task (format: YYYY-MM-DD). |
| `label` |required| Name of this task. |

### Request

`GET /schedule/addTask/onetime`

    localhost:5000//schedule/addTask/onetime?stream=1&list=bird.mp4&starttime=10:00&endtime=13:00&startdate=2024-04-12&label=LISTVIDEO2

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

