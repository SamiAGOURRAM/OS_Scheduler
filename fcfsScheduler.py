from NonPreemptiveScheduler import NonPreemptiveScheduler

class fcfsScheduler(NonPreemptiveScheduler):
    """
    First-Come, First-Served (FCFS) scheduling algorithm.
    """
    def __init__(self):
        super().__init__()

    def push_to_queue(self, i, p):
        self.ready_queue.append(i)

    def pop_from_queue(self, processes):
        i = self.ready_queue[0]
        self.ready_queue.pop(0)
        return i, processes[i]