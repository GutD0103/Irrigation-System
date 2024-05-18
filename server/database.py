import sqlite3
from TaskInfor import TaskInformation

class TaskDatabase:
    def __init__(self, db_name, table_name="tasks"):
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                              ID INTEGER PRIMARY KEY,
                              label TEXT,
                              mixer TEXT,
                              area TEXT,
                              duration INTEGER,
                              start_date TEXT,
                              until TEXT,
                              start_time TEXT,
                              end_time TEXT,
                              typetask TEXT,
                              days TEXT
                              )''')
        self.conn.commit()

    def add_task(self, task_info):
        self.cursor.execute(f"INSERT INTO {self.table_name} ( label, days, mixer,area , duration, start_date, until, start_time, end_time, typetask) VALUES ( ?, ?, ?,?, ?, ?, ?, ?, ?, ?)",
                            ( task_info.label, ','.join(str(item) for item in task_info.days), ','.join(str(item) for item in task_info.mixer),','.join(str(item) for item in task_info.area), task_info.duration, task_info.start_date, task_info.until, task_info.start_time, task_info.end_time, task_info.typetask))
        self.conn.commit()
        last_row_id = self.cursor.lastrowid
        print(f"The ID of the last inserted row is: {last_row_id}")
        return last_row_id

    def delete_task(self, ID=None, label=None):
        if ID is not None and ID != 0:
            self.cursor.execute(f"DELETE FROM {self.table_name} WHERE ID=?", (ID,))
            self.conn.commit()
            print(f"Deleted task with ID {ID}.")
        elif label is not None:
            self.cursor.execute(f"DELETE FROM {self.table_name} WHERE label=?", (label,))
            self.conn.commit()
            print(f"Deleted task with label {label}.")
        else:
            print("No task deleted. Please provide either ID or label.")

    def close_connection(self):
        self.conn.close()

    def get_last_id(self):
        last_row_id = self.cursor.lastrowid
        print(f"The ID of the last inserted row is: {last_row_id}")
        return last_row_id
    
    def get_all_tasks(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        tasks_data = self.cursor.fetchall()
        tasks = []
        for task_data in tasks_data:
            task = TaskInformation(*task_data)
            task.mixer = task.mixer.split(',')
            task.area = task.area.split(',')
            task.days = task.days.split(',')
            tasks.append(task)
        return tasks
    
    def delete_all_tasks(self):
        self.cursor.execute(f"DELETE FROM {self.table_name}")
        self.conn.commit()
        print("Deleted all tasks.")

def main():
    # Sử dụng lớp TaskDatabase để tạo cơ sở dữ liệu và thêm dữ liệu
    task_db = TaskDatabase('schedule.db',"schedule")

    all_tasks = task_db.get_all_tasks()
    # if all_tasks:
    #         print("Retrieved Task Information:")
    #         for task in all_tasks:
    #             print(f"ID: {task.ID}")
    #             print(f"Label: {task.label}")
    #             print(f"Days: {task.days}")
    #             print(f"Video Name: {task.video_name}")
    #             print(f"Duration: {task.duration}")
    #             print(f"Start Date: {task.start_date}")
    #             print(f"Until: {task.until}")
    #             print(f"Start Time: {task.start_time}")
    #             print(f"End Time: {task.end_time}")
    #             print(f"Type Task: {task.typetask}")
    #             print("\n")

    # # Đóng kết nối

    task_db.close_connection()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        raise