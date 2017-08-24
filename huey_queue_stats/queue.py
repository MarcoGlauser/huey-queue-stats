import re
import threading

import redis
from huey import RedisHuey
from huey.consumer import EVENT_FINISHED

from huey_queue_stats.moving_average import MovingAverage, EventPerSecondAverage


class TaskQueue:
    growing_threshold = 3

    def __init__(self, name, connection_pool):
        self.length = 0
        self.scheduled = 0
        self.name = name
        self.clean_name = self.clean_name(name)
        self.redis_queue = 'huey.redis.%s' % self.clean_name
        self.redis_schedule = 'huey.schedule.%s' % self.clean_name
        self.redis_connection = redis.Redis(connection_pool=connection_pool)
        self.event_queue = EventQueue(name=self.clean_name, connection_pool=connection_pool)
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


class EventQueue:

    prefix = 'queuecmd_'

    def __init__(self, name, connection_pool):
        self.name = name
        self.huey = RedisHuey(name, connection_pool=connection_pool)
        self.average_execution_timings = {}

        thread = threading.Thread(target=self.listen)
        thread.daemon = True
        thread.start()

    def listen(self):
        for event in self.huey.storage:
            if event['status'] == EVENT_FINISHED:
                event_name = self.clean_event_name(event['task'])

                if not self.average_execution_timings.get(event_name, False):
                    self.average_execution_timings[event_name] = {
                        'execution_time': MovingAverage(size=100),
                        'tasks_per_second': EventPerSecondAverage()
                    }

                self.calculate_averages(event_name, event)

    def calculate_averages(self, name, event):
        self.average_execution_timings[name]['execution_time'].push(event['duration'])
        self.average_execution_timings[name]['tasks_per_second'].push()

    def clean_event_name(self, name):
        return name[len(self.prefix):]

    @property
    def execution_stats(self):
        return self.average_execution_timings.copy()


