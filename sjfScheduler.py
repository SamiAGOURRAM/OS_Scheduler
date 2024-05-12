from NonPreemptiveScheduler import NonPreemptiveScheduler
import heapq


class sjfScheduler(NonPreemptiveScheduler):
    """
    Shortest Job First (SJF) scheduling algorithm.
    """
    def __init__(self):
        super().__init__()

    def push_to_queue(self, i, p):
        heapq.heappush(self.ready_queue, (p.burst_time,p.pid, p)) 

    def pop_from_queue(self, processes):
        _,_, process = heapq.heappop(self.ready_queue)
        return None, process