from Scheduler import Scheduler

class PreemptiveScheduler(Scheduler):
    """
    Abstract class for preemptive scheduling algorithms.
    """
    def __init__(self, quantum=4):
        super().__init__()
        self.quantum = quantum

    def no_preemption(self, process):
        """
        Determine if preemption should occur for a process.

        Args:
            process (Process): The process to be checked.

        Returns:
            bool: True if preemption should not occur, False otherwise.
        """
        return process.remaining_time <= self.quantum