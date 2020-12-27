import time
import functools

class TimerException(Exception):
    # Custom exception class used to report timer errors
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

class Timer:
    def __init__(self, logging=print, msg="Elapsed time: {:0.4f} s"):
        self._start_time = None
        self._logging = logging
        self._msg = msg

    def Start(self) -> float:
        if self._start_time is not None:
            raise TimerException("Timer already running. Stop first.")

        self._start_time = time.perf_counter()

    def Stop(self):
        if self._start_time is None:
            raise TimerException("Timer not running. Start timer first.")
        
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        if self._logging:
            self._logging(self._msg.format(elapsed_time))
        return elapsed_time

    def __enter__(self):
        self.Start()
        return self

    def __exit__(self, *exec_info):
        self.Stop()

    def __call__(self, func):
        # Support using Timer as decorator
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper_timer