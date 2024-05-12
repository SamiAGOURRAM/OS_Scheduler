from PreemptiveScheduler import PreemptiveScheduler
import heapq

class PriorityRoundRobinScheduler(PreemptiveScheduler):
    """
    Priority-based Round Robin scheduling algorithm.
    """
    def __init__(self, quantum=4):

        super().__init__(quantum)
        self.counter = 0
        heapq.heapify(self.ready_queue)


    def push_to_queue(self, i, p):
        heapq.heappush(self.ready_queue, (p.priority, self.counter, p)) 
        self.counter += 1


    def pop_from_queue(self, processes):
        _,_, process = heapq.heappop(self.ready_queue)
        return None, process