import os
from tabulate import tabulate

from huey_queue_stats.queue import TaskQueue


class Printer:
    def __init__(self, queues):
        self.queue_printers = [QueuePrinter(queue) for queue in queues]

    def format_queue_string(self):
        formatted_queue_strings = [queue_printer.format_string() for queue_printer in self.queue_printers]
        return ''.join(formatted_queue_strings)

    @classmethod
    def clear(cls):
        os.system('clear')


class QueuePrinter:
    def __init__(self, queue: TaskQueue):
        self.queue = queue
        self.layout = '-' * 40 + '\n' + \
                      queue.name + ' - ' + queue.redis_queue + '\n' + \
                      '-' * 40 + '\n' + \
                      '{queue_length_visualization}\n' + \
                      'Queued: {queue_length} {queue_length_change_sign} \n' + \
                      'Scheduled: {scheduled_length}\n\n' + \
                      '{execution_stats}\n' + \
                      '\n\n'

    def format_string(self):
        return self.layout.format(
            queue_length_visualization=self._format_queue_length_visualization(),
            queue_length=self.queue.length,
            queue_length_change_sign=self._format_queue_length_change_sign(),
            scheduled_length=self.queue.scheduled,
            execution_stats=self._format_execution_stats()
        )

    def _format_execution_stats(self,):
        tabulate_headers = ['Task' + ' ' * 22, 'Avg Time(ms)', 'Task/min']
        tasks = sorted(self.queue.event_queue.execution_stats.items())
        tabulate_items = map(lambda item: [
            item[0],
            round(item[1]['execution_time'].value * 1000),
            round(item[1]['tasks_per_second'].value, 2)
        ], tasks)
        return tabulate(tabulate_items, tabulate_headers, tablefmt="plain")

    def _format_queue_length_visualization(self):
        return '|' * min(50, self.queue.length)

    def _format_queue_length_change_sign(self):
        if self.queue.is_growing():
            return '+'
        elif self.queue.is_shrinking():
            return '-'
        else:
            return '='
