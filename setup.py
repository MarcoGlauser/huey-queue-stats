from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='huey_queue_stats',
      version='0.2.0',
      description='Shows basic information about one or more huey queues',
      author='Adtech @ APG SGA AG',
      author_email='marco.glauser@apgsga.ch',
      license='MIT',
      packages=['huey_queue_stats'],
      install_requires=required,
      entry_points={
          'console_scripts': [
              'huey_stats = huey_queue_stats.huey_queue_stats:main'
          ]
      }
)
