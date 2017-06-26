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
@click.option('--queue', '-q', multiple=True, required=True, help='Name of the queue to print stats about. There can be multiple -q arguments.')
@click.option('--refresh-rate', '-r', default=0.5, help='Stats refresh rate in seconds')
def display_redis_stats(connection_string, queue, refresh_rate):
    os.system('clear')
    print('Connecting to redis...')
    r = redis.Redis.from_url(connection_string, max_connections=10)
    queues = build_queue_dict(queue)

    while True:
        for queue in queues:
            queue['length'] = r.llen(queue['redis_queue'])
            queue['scheduled'] = r.zcard(queue['redis_schedule'])

        os.system('clear')
        for queue in queues:
            print('-'*40)
            print(queue['name'] + ' - ' + queue['redis_queue'])
            print('-'*40)
            print('|' * min(100, queue['length']))
            print('Queued: %s' % queue['length'])
            print('Scheduled: %s' % queue['scheduled'])
            print('\n\n')

        time.sleep(refresh_rate)


def build_queue_dict(queue_names):
    queues = []
    for queue_name in queue_names:
        queue_dict = {
            'name': queue_name,
            'clean_name': clean_name(queue_name)
        }
        queue_dict['redis_queue'] = 'huey.redis.%s' % queue_dict['clean_name']
        queue_dict['redis_schedule'] = 'huey.schedule.%s' % queue_dict['clean_name']
        queues.append(queue_dict)
    return queues


# Copied from https://github.com/coleifer/huey/blob/master/huey/storage.py#L139
def clean_name(name):
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
