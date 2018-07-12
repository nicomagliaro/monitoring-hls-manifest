# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .housekeep import Housekeep

logger = get_task_logger(__name__)

@periodic_task(
                run_every=(crontab(minute='*/1')),
                name="delete_old_stuff",
                ignore_result=True
)
def delete_tmp_dirs():
    """ Delete zombie dirs undeleted because timeouts request"""
    delete_tmp = Housekeep()
    delete_tmp.delete_old()
    logger.info("/var/tmp/hls directory housekeeped")