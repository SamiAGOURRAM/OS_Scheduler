from Scheduler import Scheduler

class NonPreemptiveScheduler(Scheduler):
    """
    Abstract class for non-preemptive scheduling algorithms.
    """

    def __init__(self):
        super().__init__()

    def no_preemption(self, process):
        """
        Determine if preemption should occur for a process (always returns True).

        Args:
            process (Process): The process to be checked.

        Returns:
            bool: True (non-preemptive).
        """
        return True