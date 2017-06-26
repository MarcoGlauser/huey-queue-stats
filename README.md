# huey-queue-stats
This script gives you some basic information about the queues and schedules used by huey.

```bash
Usage: huey_queue_stats.py [OPTIONS]

Options:
  -c, --connection-string TEXT  Connection string to redis including database.
                                for example redis://localhost:6379/0
                                [required]
  -q, --queue TEXT              Name of the queue to print stats about. There
                                can be multiple -q arguments.  [required]
  -r, --refresh-rate FLOAT      Stats refresh rate in seconds
  --help                        Show this message and exit.

```


Example: 
```bash
source venv/bin/activate
./huey_queue_stats.py -c redis://localhost:6379/0 -q huey1 -q huey2
```