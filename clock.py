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


@sched.scheduled_job('interval', minutes=15)
def sync_docs():
    print('Running Syncdocs')

    subprocess.call(['python', 'manage.py', 'syncdocs'], stderr=sys.stderr, stdout=sys.stdout)

sched.start()
