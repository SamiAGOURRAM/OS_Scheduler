from input import read_processes_from_file
from fcfsScheduler import fcfsScheduler
from sjfScheduler import sjfScheduler
from RoundRobinScheduler import RoundRobinSheduler
from priorityScheduler import priorityScheduler
from PriorityRoundRobinScheduler import PriorityRoundRobinScheduler


quantum = 4

test_dic = {"FCFS" : fcfsScheduler(), "SJF" : sjfScheduler(), "Priority Scheduling" : priorityScheduler(),
            "Round Robin - quantum :" +str(quantum) : RoundRobinSheduler(quantum), "Priority + RR - quantum : " + str(quantum) : PriorityRoundRobinScheduler(quantum) }

for i in test_dic.keys():
    
    processes = read_processes_from_file("processes.csv")

    print(i )
    print('------------------')

    test_dic[i].schedule(processes)
    test_dic[i].output(processes)
    print("-------------------")
    print("Gantt chart")
    print(test_dic[i].gant_chart)

    print("---------------------")



















