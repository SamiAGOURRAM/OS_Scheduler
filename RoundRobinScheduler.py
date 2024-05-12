from PreemptiveScheduler import PreemptiveScheduler

class RoundRobinSheduler(PreemptiveScheduler):
    """
    Round Robin scheduling algorithm.
    """
    def __init__(self, quantum=4):
        super().__init__(quantum=4)

    def push_to_queue(self, i, p):
        self.ready_queue.append(i)

    def pop_from_queue(self, processes):
        i = self.ready_queue[0]
        self.ready_queue.pop(0)
        return i, processes[i]