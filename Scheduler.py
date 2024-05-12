from process import Process
from abc import ABC, abstractmethod
from input import read_processes_from_file

class Scheduler(ABC):
    """
    Abstract Base Class for implementing scheduling algorithms.

    Attributes:
        ready_queue (list): A list representing the ready queue of processes.
        programs_executed (int): The number of programs executed.
        current_time (int): The current simulation time.
        gant_chart (dict): A dictionary representing the Gantt chart.
    """

    def __init__(self):
        """Initialize the Scheduler."""
        self.ready_queue = []
        self.programs_executed = 0
        self.current_time = 0
        self.gant_chart = {}
    
    def check_for_new_arrivals(self, processes):
        """
        Check for new arrivals and add them to the ready queue if applicable.

        Args:
            processes (list): List of processes to be checked.
        """
        if self.programs_executed == len(processes):
            return
        for i in range(len(processes)):
            p = processes[i]
            if p.arrival_time <= self.current_time and not p.in_queue and not p.is_complete:  
                    self.push_to_queue(i, p)
                    processes[i].in_queue = True

    def update_queue(self, processes):
        """
        Update the ready queue based on the scheduling algorithm.

        Args:
            processes (list): List of processes.
        """
        if self.ready_queue:

            i, process = self.pop_from_queue(processes)

            if self.no_preemption(process):
                process.is_complete = True
                process.in_queue = False
                self.gant_chart[(self.current_time, self.current_time + process.remaining_time )] = process
                self.current_time += process.remaining_time

                process.completion_time = self.current_time
                process.waiting_time = process.completion_time - process.arrival_time - process.burst_time
                process.turnAround_time = process.waiting_time + process.burst_time
                process.remaining_time = 0
                self.programs_executed += 1

                if process.waiting_time < 0:
                    process.waiting_time = 0
                self.check_for_new_arrivals(processes)

            else:
                process.remaining_time -= self.quantum
                self.gant_chart[(self.current_time, self.current_time + self.quantum )] = process

                self.current_time += self.quantum

                self.check_for_new_arrivals(processes)

                self.push_to_queue(i, process)

                process.in_queue = True

        else:
            interval_start = self.current_time
            while not self.ready_queue:
                self.current_time += 1
                self.check_for_new_arrivals(processes)
            interval_end = self.current_time

            self.gant_chart[(interval_start, interval_end)] = "idle"





            
        

    @abstractmethod
    def push_to_queue(self, i, p):
        """
        Abstract method to push a process into the ready queue.

        Args:
            i (int): Index of the process.
            p (Process): The process to be pushed into the ready queue.
        """
        pass

    @abstractmethod
    def pop_from_queue(self,processes):
        """
        Abstract method to pop a process from the ready queue.

        Args:
            processes (list): List of processes.

        Returns:
            tuple: Tuple containing index of the process and the process itself.
        """
        pass

    @abstractmethod
    def no_preemption(self, process):
        """
        Abstract method to determine if preemption should occur for a process.

        Args:
            process (Process): The process to be checked.

        Returns:
            bool: True if preemption should not occur, False otherwise.
        """
        pass

    def schedule(self, processes):
        """
        Schedule the processes using the implemented scheduling algorithm.

        Args:
            processes (list): List of processes to be scheduled.
        """
        processes.sort(key=lambda x : x.arrival_time)
        self.check_for_new_arrivals(processes)
        while self.programs_executed < len(processes):
            self.update_queue(processes)

    def output(self,processes):
        """
        Output the scheduling results.

        Args:
            processes (list): List of processes.
        """
        avg_waiting_time = 0
        avg_turntaround_time = 0
        # sort the processes array by processes.PID
        processes.sort(key=lambda p: p.pid)
    
        for i in range(len(processes)):
            print("Process ", processes[i].pid, ": Waiting Time: ", processes[i].waiting_time,
                " Turnaround Time: ", processes[i].turnAround_time, sep="")
            avg_waiting_time += processes[i].waiting_time
            avg_turntaround_time += processes[i].turnAround_time
        print("Average Waiting Time: ", avg_waiting_time / len(processes))
        print("Average Turnaround Time: ", avg_turntaround_time / len(processes))