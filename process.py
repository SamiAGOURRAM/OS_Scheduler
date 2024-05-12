
class Process:

    def __init__(self,pid,arrival_time,burst_time,priority=None,completion_time = 0,waiting_time = 0,turnAround_time = 0,in_queue = False,is_complete = False):
        self.pid=pid # This is process ID
        self.arrival_time=arrival_time #This is the arrival time of the process
        self.burst_time=burst_time # The required CPU time for a process
        self.priority=priority  # The process priority that we will use in the priority algorithm
        self.remaining_time=burst_time  # the remaining burst time,it is initially equal to burst time
        self.completion_time=completion_time
        self.waiting_time=waiting_time
        self.turnAround_time=turnAround_time
        self.in_queue=in_queue
        self.is_complete=is_complete
    def reset(self): 
        self.remaining_time = self.burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnAround_time = 0
        self.in_queue = False
        self.is_complete = False
    def __repr__(self):
        return f"Process(pid={self.pid},arrival_time={self.arrival_time},burst_time={self.burst_time},priority={self.priority})"