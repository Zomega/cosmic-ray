from cosmic_ray.execution.execution_engine import ExecutionEngine
from cosmic_ray.work_record import WorkRecord

from .app import app
from .worker import execute_work_records


# pylint: disable=too-few-public-methods
class CeleryExecutionEngine(ExecutionEngine):
    def __call__(self, timeout, pending_work, config):
        purge_queue = config['execution-engine'].get('purge-queue', True)

        try:
            results = execute_work_records(
                timeout,
                pending_work,
                config)

            for result in results:
                yield WorkRecord(result)
        finally:
            if purge_queue:
                app.control.purge()
