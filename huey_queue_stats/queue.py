import re

class Queue:
    length = 0
    scheduled = 0
    name = ''

    def __init__(self, name, redis_connection):
        self.name = name
        self.clean_name = self.clean_name(name)
        self.redis_queue = 'huey.redis.%s' % self.clean_name
        self.redis_schedule = 'huey.schedule.%s' % self.clean_name
        self.redis_connection = redis_connection
        self.update()

    def update(self):
        self.length = self.redis_connection.llen(self.redis_queue)
        self.scheduled = self.redis_connection.zcard(self.redis_schedule)

    # Copied from https://github.com/coleifer/huey/blob/master/huey/storage.py#L139
    def clean_name(self, name):
        return re.sub('[^a-z0-9]', '', name)