#!/usr/bin/env python
import os

import click
import redis
import time

from huey_queue_stats.printer import Printer

from .queue import TaskQueue


@click.command()
@click.option('--connection-string', '-c',
              default='redis://localhost:6379',
              help='Connection string to redis including database. for example redis://localhost:6379/0'
              )
@click.option('--queue_names', '-q', multiple=True, required=True, help='Name of the queues to print stats about. There can be multiple -q arguments.')
@click.option('--refresh-rate', '-r', default=0.5, help='Stats refresh rate in seconds')
@click.version_option()
def display_redis_stats(connection_string, queue_names, refresh_rate):
    Printer.clear()
    print('Connecting to redis...')
    pool = redis.BlockingConnectionPool.from_url(
            connection_string,
            max_connections=5,
            timeout=10
    )
    queues = [TaskQueue(queue_name, pool) for queue_name in queue_names]
    printer = Printer(queues)
    while True:
        [queue.update() for queue in queues]

        Printer.clear()
        print(printer.format_queue_string())
        time.sleep(refresh_rate)


def main():
    os.system('setterm -cursor off')
    try:
        display_redis_stats()
    except KeyboardInterrupt:
        Printer.clear()
        print('\n')
    finally:
        os.system('setterm -cursor on')


if __name__ == "__main__":
    main()
