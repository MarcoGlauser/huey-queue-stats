#!/usr/bin/env python
import os

import click
import redis
import time

from .queue import Queue


@click.command()
@click.option('--connection-string', '-c',
              default='redis://localhost:6379',
              help='Connection string to redis including database. for example redis://localhost:6379/0'
              )
@click.option('--queue_names', '-q', multiple=True, required=True, help='Name of the queues to print stats about. There can be multiple -q arguments.')
@click.option('--refresh-rate', '-r', default=0.5, help='Stats refresh rate in seconds')
@click.version_option()
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
            print('Queued: %s %s' % (queue.length, queue_size_change_sign(queue)))
            print('Scheduled: %s' % queue.scheduled)
            print('\n\n')

        time.sleep(refresh_rate)


def queue_size_change_sign(queue):
    if queue.is_growing():
        return '+'
    elif queue.is_shrinking():
        return '-'
    else:
        return '='


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
