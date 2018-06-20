'''
Tests for the ``job`` module.
'''

from unittest.mock import Mock
import pytest

from .old.Exceptions import JobNotCallableException
from .job import Job


def test_job_bad_init(event_loop):
    '''
    Test an exception is raises when a Job is created without a callable.
    '''
    with pytest.raises(JobNotCallableException):
        Job(event_loop, None, 0)


def test_job_init_before_loop_start(loop):
    '''
    Test a job being called before the loop is started.
    '''
    action = Mock(side_effect=loop.stop)

    job = Job(loop, action, 0)
    action.assert_not_called()

    # run the job
    job()

    loop.run()

    action.assert_called_once_with()


@pytest.mark.asyncio
async def test_init_after_loop_start(loop):
    '''
    Test a job being called after the loop is started.
    '''
    action = Mock()

    job = Job(loop, action, 0)
    await loop.sleep(0)
    action.assert_not_called()

    # run the job
    job()
    await loop.sleep(0)
    action.assert_called_once_with()


def test_job_no_start(loop):
    '''
    Test a job is not being called without explicit telling it so.
    '''
    action = Mock()
    action.side_effect = loop.stop

    Job(loop, action, 0)
    action.assert_not_called()

    # do not run the job

    with pytest.raises(pytest.AsyncioTimeout):
        loop.run(1)

    action.assert_not_called()


@pytest.mark.parametrize("sched_time", [0, 1, 1e24])
def test_get_scheduled_time(loop, sched_time):
    '''
    Test the ``get_scheduled_time`` method returns the proper value.
    '''
    action = Mock()
    job = Job(loop, action, sched_time)

    assert job.get_scheduled_time() == sched_time
