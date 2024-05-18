import json
from datetime import datetime, time, timedelta

class TaskInformation:
    def __init__(self, ID , label, days ,mixer, area,duration,start_date,until, start_time, end_time ,typetask ):
        self.ID = ID
        self.label = label
        self.mixer = mixer
        self.area = area
        self.duration = duration
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        self.until = datetime.strptime(until, "%Y-%m-%d %H:%M:%S")
        self.start_time  = start_time
        self.end_time = end_time
        self.typetask = typetask
        self.days = days
        


    def __str__(self):
            return f"ID: {self.ID}, Video Name: {', '.join(self.video_name)}"
    
    def to_json(self):
        return {
            'id' : self.ID,
            'label': self.label,
            'mixer': self.mixer,
            'area': self.area,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
    
def test():
    task_info = TaskInformation(
    ID=1,
    label='Test Task',
    days=['Monday', 'Wednesday', 'Friday'],
    mixer='Mixer A',
    area='Area 1',
    duration=120,
    start_date='2024-05-18 08:00:00',
    until='2024-05-18 10:00:00',
    start_time='08:00',
    end_time='10:00',
    typetask='Type A'
    )

    # Trích xuất các giá trị cần thiết và đóng gói vào một từ điển
    print(task_info.to_json())

if __name__ == "__main__":
    test()
