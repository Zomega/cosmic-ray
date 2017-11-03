"""Celery specific details for routing work requests to Cosmic Ray workers."""

import celery
from celery.utils.log import get_logger

from cosmic_ray.worker import worker_process

from .app import app

LOG = get_logger(__name__)


@app.task(name='cosmic_ray_celery4_engine.worker')
def worker_task(work_record,
                timeout,
                config):
    """The celery task which performs a single mutation and runs a test suite.

    This runs `cosmic-ray worker` in a subprocess and returns the results,
    passing `config` to it via stdin.

    Returns: An updated WorkRecord

    """
    return worker_process(work_record, timeout, config)


def execute_work_records(timeout,
                         work_records,
                         config):
    """Execute a suite of tests for a given set of work items.

    Args:
      timeout: The max length of time to let a test run before it's killed.
      work_records: An iterable of `work_db.WorkItem`s.
      config: The configuration to use for the test execution.

    Returns: An iterable of WorkRecords.
    """
    return celery.group(
        worker_task.s(work_record,
                      timeout,
                      config)
        for work_record in work_records)().get()
