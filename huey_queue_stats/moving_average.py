import time

from collections import deque
from datetime import timedelta


class MovingAverage:

    def __init__(self, size=5):
        self.values = deque(maxlen=size)

    def push(self, value):
        self.values.append(value)

    @property
    def value(self):
        length = len(self.values)
        if length > 0:
            return sum(self.values) / length
        else:
            return 0

    def __len__(self):
        return len(self.values)


class EventPerSecondAverage:
    max_lifetime = timedelta(minutes=30)

    def __init__(self):
        self.events = deque(maxlen=1000)

    def push(self):
        self.events.append(time.time())
        self.remove_stale_events()

    def remove_stale_events(self):
        try:
            event_is_older_than_max_lifetime = self.events[0] + self.max_lifetime.seconds < time.time()
            while event_is_older_than_max_lifetime:
                self.events.popleft()
        except IndexError:
            pass

    @property
    def value(self):
        self.remove_stale_events()

        if len(self.events) > 0:
            time_span = (time.time() - self.events[0]) / 60
            return len(self.events) / time_span
        else:
            return 0
