from __future__ import absolute_import, unicode_literals, division, print_function
import logging
logging.basicConfig()

__author__ = 'reyrodrigues'

from apscheduler.schedulers.blocking import BlockingScheduler
import os
import subprocess
sched = BlockingScheduler()

import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@sched.scheduled_job('interval', minutes=1)
def one_minute():
    subprocess.call(['python', 'manage.py', 'syncdocs'], stderr=sys.stderr, stdout=sys.stdout)

    print('This job is run every three minutes.')

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
