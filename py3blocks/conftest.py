'''
conftest.py is not needed for py3blocks but configures and prepeares some
things for testing with pytest.
'''

import asyncio
import pytest


class AsyncioTimeout(BaseException):
    '''
    Exception for an asyncio loop that took longer than the configured timeout
    allows.
    '''

    def __init__(self, timeout):
        super().__init__("Timeout of {}s reached!".format(timeout))


pytest.AsyncioTimeout = AsyncioTimeout


@pytest.fixture(scope='function')
def loop(event_loop):
    '''Provides an event_loop that can run with a configured timeout.'''

    def sleep(delay):
        '''Sleeps the loop for the configured delay.'''
        return asyncio.sleep(delay, loop=event_loop)
    event_loop.sleep = sleep

    def run(timeout=5):
        '''
        Runs the event_loop with a ``timeout`` in seconds.
        An ``pytest.AsyncioTimeout`` will be raised inside the loop once the
        timeout is reached.
        '''
        def timeout_reached():
            '''
            Will be called once the timeout is reached an raises an
            ``pytest.AsyncioTimeout``.
            '''
            raise AsyncioTimeout(timeout)
        event_loop.call_later(delay=timeout, callback=timeout_reached)
        event_loop.run_forever()

    event_loop.run = run
    yield event_loop
