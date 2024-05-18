# API Documentation

## Overview
This API provides endpoints for managing tasks related to streaming, such as retrieving video files, setting stream keys, scheduling live streams, and managing scheduled tasks.

## Install


## Run the app

    start run.bat

# REST API FOR SCHEDULER

The REST API to the example app is described below.

## Get list of Video
Retrieves a list of video names availabel for streaming.
### Request

`GET /get/video`

    localhost:5000//get/video

### Response
Success: Returns a JSON object containing the schedule details.

    "Video name": [
        "bird.mp4",
        "horse.mp4",
        "idle.mp4",
        "ship.mp4"
    ]

## Get Schedule
Retrieves the schedule of streaming tasks.

### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `stream` | required, defaul = 1 | Choose a streaming channel. |
### Request

`GET /get/schedule`

    localhost:5000//get/schedule?stream=1

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
## Get Stream Key
Retrieves the stream key used for streaming.
### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `stream` | required, defaul = 1 | Choose a streaming channel. |

### Request

`GET /get/streamkey`

    localhost:5000//get/streamkey?stream=1

### Response
Success: Returns a JSON object containing the stream key.

    "Stream key": "live_1039732177_vlmsO93WolB9ky25idCbI6fnEBMnX233"

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

## Set Stream Key
Sets the stream key for streaming.
### Request

`GET /set/streamkey`

    localhost:5000//set/streamkey?streamkey=my_stream_key

### Response
Success: Returns a JSON object containing the stream key.

    "success": {
         "message": "Set stream key success"
    }

## Live Stream
Initiates a live stream with provided video list

### Query Parameters:
| Parameter| Requirement | Description |
| --- | --- | --- |
| `list` | required | Comma-separated list of video names. |
| `stream` | required, defaul = 1 | Choose a streaming channel. |
### Request

`GET /live?{list_video}`

    localhost:5000//live?list=bird.mp4,ship.mp4&stream=1

### Response
Success: Returns a JSON object containing the stream key.
    
    "success": {
        "message": "Live stream"
    }

## Stop Live Stream
Stops the ongoing live stream.

### Request

`GET /stoplive`

    localhost:5000//stoplive?stream=1

### Response
Success: Returns a JSON object containing the stream key.
    
    "success": {
        "message": "Stop live stream"
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

Deletes a streaming task by ID.

### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `stream` | required, defaul = 1 | Choose a streaming channel. |
| `id` | optional | ID of the task to delete, or "all" to delete all tasks. |
| `label` | optional| Name of this task. |

* This request requires at least 1 parameter.
### Request

`GET /schedule/deleteTask`

    localhost:5000//schedule/deleteTask?stream=1&id=1&label=VIDEO1

### Response
Success: Returns a success message along with the ID of the created task.
    
    "success": {
       "message": "Delete task",
       "ID": 1
     }

# REST API FOR SETTING STREAM FOR POLE

The REST API to the example app is described below.

## Retrieve Pole Information
Retrieves information about poles.
### Request

`GET /get/pole`

    localhost:5000//get/pole

### Response
Returns JSON data containing information about poles.

    {
        "Pole infomation": [
            {
                "ID": 1,
                "location": "123123:12321312",
                "infor": "VIP",
                "area": "HCMUT03",
                "link": "https://www.twitch.tv/gutsssssssss9"
            },
            {
                "ID": 2,
                "location": "12:13",
                "infor": "VIP",
                "area": "HCMUT03",
                "link": "https://www.twitch.tv/gutsssssssss9"
            },
            {
                "ID": 3,
                "location": "12:14",
                "infor": null,
                "area": "HCMUT03",
                "link": "https://www.twitch.tv/gutsssssssss9"
            },
            {
                "ID": 4,
                "location": "13:13",
                "infor": null,
                "area": "HCMUT02",
                "link": "https://www.twitch.tv/huynhnguyenhieunhan"
            },
            {
                "ID": 5,
                "location": "12:12",
                "infor": null,
                "area": "HCMUT02",
                "link": "https://www.twitch.tv/huynhnguyenhieunhan"
            },
            {
                "ID": 6,
                "location": "12:17",
                "infor": null,
                "area": "HCMUT02",
                "link": "https://www.twitch.tv/huynhnguyenhieunhan"
            },
            {
                "ID": 7,
                "location": "15:15",
                "infor": null,
                "area": "HCMUT01",
                "link": "https://www.twitch.tv/huynhnguyenhieunhan"
            },
            {
                "ID": 8,
                "location": "12:65",
                "infor": null,
                "area": "HCMUT01",
                "link": "https://www.twitch.tv/huynhnguyenhieunhan"
            },
            {
                "ID": 9,
                "location": "14:14",
                "infor": null,
                "area": "HCMUT01",
                "link": "https://www.twitch.tv/huynhnguyenhieunhan"
            },
            {
                "ID": 10,
                "location": "32:32",
                "infor": null,
                "area": "HCMUT01",
                "link": "https://www.twitch.tv/huynhnguyenhieunhan"
            }
        ]
    }

## Set Pole Area
Sets the area of specified poles.
### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `ID` | required| Comma-separated list of pole IDs. |
| `area` | required| New area to set for the poles. |

### Request

`GET /set/poleArea`

    localhost:5000//set/poleArea?ID=7,8,9,10&area=HCMUT01

### Response
Success: Returns a success message if the operation is successful.

    {
        "success": {
            "message": "Update success"
        }
    }

##  Set Pole Link by ID
 Sets livestream link for specified poles by their IDs.
### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `ID` | required| Comma-separated list of pole IDs. |
| `stream` | required| Specifies the livestream source (1 or 2).|

### Request

`GET /set/poleStream/ID`

    localhost:5000//set/poleStream/ID?ID=1,2,3&stream=1

### Response
Success: Returns a success message if the operation is successful.

    {
        "success": {
            "message": "Set stream"
        }
    }

##  Set Pole Link by Area
Sets livestream link for poles in a specific area.
### Query Parameters:

| Parameter| Requirement | Description |
| --- | --- | --- |
| `area` | required|  Area where poles are located. |
| `stream` | required| Specifies the livestream source (1 or 2).|

### Request

`GET /set/poleStream/area`

    localhost:5000//set/poleLink/area?area=HCMUT02&stream=1
    
### Response
Success: Returns a success message if the operation is successful.

    {
        "success": {
            "message": "Set stream"
        }
    }
