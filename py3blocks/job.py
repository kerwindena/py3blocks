'''
Module that contains the definition of a ``Job``.
'''

import asyncio

from .old.Exceptions import JobNotCallableException


class Job:
    '''
    Job wraps a callback to be run at a later time.
    It also contains a time when the job is to be run.
    '''

    def __init__(self,
                 event_loop: asyncio.AbstractEventLoop,
                 action: callable,
                 scheduled_time: float):
        if not callable(action):
            raise JobNotCallableException()
        self.__event_loop = event_loop
        self.__action = action
        self.__scheduled_time = scheduled_time

    def call(self):
        '''Executes the job ignoring the ``scheduled_time``.'''
        self.__event_loop.call_soon_threadsafe(self.__action)

    def get_scheduled_time(self):
        '''Gets the time when the job is scheduled.'''
        return self.__scheduled_time

    def __call__(self):
        self.call()
