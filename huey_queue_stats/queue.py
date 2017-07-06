import re

from .moving_average import MovingAverage


class Queue:
    length = 0
    scheduled = 0
    name = ''
    average = None
    growing_threshold = 3

    def __init__(self, name, redis_connection):
        self.name = name
        self.clean_name = self.clean_name(name)
        self.redis_queue = 'huey.redis.%s' % self.clean_name
        self.redis_schedule = 'huey.schedule.%s' % self.clean_name
        self.redis_connection = redis_connection
        self.average = MovingAverage(size=10)
        self.update()

    def update(self):
        self.length = self.redis_connection.llen(self.redis_queue)
        self.average.push(self.length)
        self.scheduled = self.redis_connection.zcard(self.redis_schedule)

    def is_growing(self):
        return self.length > self.average.value + self.growing_threshold

    def is_shrinking(self):
        return self.length < self.average.value - self.growing_threshold

    # Copied from https://github.com/coleifer/huey/blob/master/huey/storage.py#L139
    def clean_name(self, name):
        return re.sub('[^a-z0-9]', '', name)