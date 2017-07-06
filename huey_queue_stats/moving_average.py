from collections import deque


class MovingAverage:

    def __init__(self, size=5):
        self.values = deque()
        self.size = size

    def push(self, value):
        self.values.append(value)
        if len(self.values) > self.size:
            self.values.popleft()

    @property
    def value(self):
        length = len(self.values)
        if not length:
            return 0
        else:
            return sum(self.values) / length

    def __float__(self):
        return self.value