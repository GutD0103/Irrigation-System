import time
from threading import Timer

SCH_MAX_TASKS = 40  # Adjust based on your requirements
NO_TASK_ID = 0

class sTask:
    def __init__(self, pTask=None, Delay=0, Period=0, RunMe=0, TaskID=0):
        self.pTask = pTask
        self.Delay = Delay
        self.Period = Period
        self.RunMe = RunMe
        self.TaskID = TaskID
        
class Scheduler:
    def __init__(self, pTask=None, Delay=0, Period=0, RunMe=0, TaskID=0):

        self.TICK = 100
        self.SCH_tasks_G = [sTask() for _ in range(SCH_MAX_TASKS)]
        self.newTaskID = 0

    def Get_New_Task_ID(self):
        self.newTaskID += 1
        if self.newTaskID == NO_TASK_ID:
            self.newTaskID += 1
        return self.newTaskID

    def SCH_Init():
        pass  # Do nothing

    def SCH_Update(self):
        if self.SCH_tasks_G[0].pTask and self.SCH_tasks_G[0].RunMe == 0:
            if self.SCH_tasks_G[0].Delay > 0:
                self.SCH_tasks_G[0].Delay -= 1
            if self.SCH_tasks_G[0].Delay <= 0:
                self.SCH_tasks_G[0].RunMe = 1

    def SCH_Add_Task(self,pFunction, DELAY, PERIOD):
        sumDelay = 0
        newDelay = 0


        for newTaskIndex in range(SCH_MAX_TASKS):
            sumDelay += self.SCH_tasks_G[newTaskIndex].Delay
            if sumDelay > DELAY:
                newDelay = DELAY - (sumDelay - self.SCH_tasks_G[newTaskIndex].Delay)
                self.SCH_tasks_G[newTaskIndex].Delay = sumDelay - DELAY

                for i in range(SCH_MAX_TASKS - 1, newTaskIndex, -1):

                    self.SCH_tasks_G[i].pTask = self.SCH_tasks_G[i - 1].pTask
                    self.SCH_tasks_G[i].Period = self.SCH_tasks_G[i - 1].Period
                    self.SCH_tasks_G[i].Delay = self.SCH_tasks_G[i - 1].Delay
                    self.SCH_tasks_G[i].TaskID = self.SCH_tasks_G[i - 1].TaskID

                self.SCH_tasks_G[newTaskIndex].pTask = pFunction
                self.SCH_tasks_G[newTaskIndex].Delay = newDelay
                self.SCH_tasks_G[newTaskIndex].Period = PERIOD
                self.SCH_tasks_G[newTaskIndex].RunMe = 1 if self.SCH_tasks_G[newTaskIndex].Delay == 0 else 0
                self.SCH_tasks_G[newTaskIndex].TaskID = self.Get_New_Task_ID()
                return self.SCH_tasks_G[newTaskIndex].TaskID
            else:
                if self.SCH_tasks_G[newTaskIndex].pTask is None:
                    self.SCH_tasks_G[newTaskIndex].pTask = pFunction
                    self.SCH_tasks_G[newTaskIndex].Delay = DELAY - sumDelay
                    self.SCH_tasks_G[newTaskIndex].Period = PERIOD
                    self.SCH_tasks_G[newTaskIndex].RunMe = 1 if self.SCH_tasks_G[newTaskIndex].Delay == 0 else 0
                    self.SCH_tasks_G[newTaskIndex].TaskID = self.Get_New_Task_ID()
                    return self.SCH_tasks_G[newTaskIndex].TaskID
                
        return self.SCH_tasks_G[newTaskIndex].TaskID

    def SCH_Delete_Task(self,taskID):
        if taskID != NO_TASK_ID:
            for taskIndex in range(SCH_MAX_TASKS):
                if self.SCH_tasks_G[taskIndex].TaskID == taskID:
                    if taskIndex != 0 and taskIndex < SCH_MAX_TASKS - 1:
                        if self.SCH_tasks_G[taskIndex + 1].pTask is not None:
                            self.SCH_tasks_G[taskIndex + 1].Delay += self.SCH_tasks_G[taskIndex].Delay
                    for j in range(taskIndex, SCH_MAX_TASKS - 1):
                        self.SCH_tasks_G[j] = self.SCH_tasks_G[j + 1]
                    self.SCH_tasks_G[-1] = sTask()
                    return True
        return False

    def SCH_Dispatch_Tasks(self):
        if self.SCH_tasks_G[0].RunMe > 0:
            self.SCH_tasks_G[0].pTask()  # Run the task
            self.SCH_tasks_G[0].RunMe = 0  # Reset / reduce RunMe flag
            temtask = self.SCH_tasks_G[0]
            self.SCH_Delete_Task(temtask.TaskID)
            if temtask.Period != 0:
                self.SCH_Add_Task(temtask.pTask, temtask.Period, temtask.Period)

