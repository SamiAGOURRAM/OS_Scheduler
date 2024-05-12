from NonPreemptiveScheduler import NonPreemptiveScheduler

import heapq

class priorityScheduler(NonPreemptiveScheduler):
    """
    Priority scheduling algorithm.
    """
    def __init__(self):
        super().__init__()

    def push_to_queue(self, i, p):
        heapq.heappush(self.ready_queue, (p.priority,p.pid, p)) 

    
    def pop_from_queue(self, processes):
        _,_, process = heapq.heappop(self.ready_queue)
        return None, process