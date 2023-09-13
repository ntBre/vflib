import time


class Timer:
    def __init__(self):
        self._start = time.time()

    def say(self, s: str):
        now = time.time()
        print(f"{s} after {now - self._start:.1f} s")
