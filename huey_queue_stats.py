#!/usr/bin/env python
import os
import re

import click
import redis
import time


@click.command()
@click.option('--connection-string', '-c',
              default='redis://localhost:6379',
              help='Connection string to redis including database. for example redis://localhost:6379/0'
              )
@click.option('--queue_names', '-q', multiple=True, required=True, help='Name of the queues to print stats about. There can be multiple -q arguments.')
@click.option('--refresh-rate', '-r', default=0.5, help='Stats refresh rate in seconds')
def display_redis_stats(connection_string, queue_names, refresh_rate):
    os.system('clear')
    print('Connecting to redis...')
    r = redis.Redis.from_url(connection_string, max_connections=10)
    queues = []

    for queue_name in queue_names:
        queues.append(Queue(queue_name, r))

    while True:
        for queue in queues:
            queue.update()

        os.system('clear')
        for queue in queues:
            print('-'*40)
            print(queue.name + ' - ' + queue.redis_queue)
            print('-'*40)
            print('|' * min(100, queue.length))
            print('Queued: %s' % queue.length)
            print('Scheduled: %s' % queue.scheduled)
            print('\n\n')

        time.sleep(refresh_rate)


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


def main():
    os.system('setterm -cursor off')
    try:
        display_redis_stats()
    except KeyboardInterrupt:
        os.system('clear')
        print('\n')
    finally:
        os.system('setterm -cursor on')


if __name__ == "__main__":
    main()
