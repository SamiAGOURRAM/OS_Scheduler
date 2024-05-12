import random
from process import Process
import csv

def generate_random_processes(num_processes,burst_time_range,arrival_time_range,priority_range=None):
    processes= []
    for pid in range(1,num_processes+1):
        arrival_time =random.randint(*arrival_time_range)
        burst_time=random.randint(*burst_time_range)
        priority= random.randint(*priority_range) if priority_range else None
        processes.append(Process(pid,arrival_time,burst_time,priority))
    return processes

def read_processes_from_file(filename):
    processes=[]
    with open(filename,'r') as file:
        for l in file:
            val =l.strip().split(',')
            pid=int(val[0])
            arrival_time =int(val[1])
            burst_time =int(val[2])
            priority = None
            if len(val)==4:
                priority =int(val[3])
            process = Process(pid,arrival_time,burst_time,priority)
            processes.append(process)
    return processes

