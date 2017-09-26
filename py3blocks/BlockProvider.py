import asyncio
import os
import time


class BlockUpdate():

    def __init__(self, loop, properties, callback):
        self.__loop = loop
        self.__properties = properties
        self.__callback = callback
        self.__timeout = self._parseTimeout()
        self.__env = self._build_env()
        self.__aborted = False
        self.__process = None
        if not callable(callback):
            raise Exception('Callback needs to be callable')

    def _build_env(self):
        env = os.environ.copy()
        for k, v in self.__properties.items():
            if v is not None:
                prop_name = 'BLOCK_{}'.format(str(k)).upper()
                env[prop_name] = str(v)
        return env

    def _parseTimeout(self):
        timeout = 120
        try:
            timeout = abs(int(self.__properties['_timeout']))
        except Exception:
            pass
        return timeout

    def __return(self, start_time, full_text='', short_text='', color=''):
        properties = self.__properties.copy()
        if len(full_text) > 0:
            properties['full_text'] = ''
            if properties['_label'] is not None and len(properties['_label']) > 0:
                properties['full_text'] = properties['_label'] + ' '
            properties['full_text'] += full_text
        if len(short_text) > 0:
            properties['short_text'] = short_text
        if len(color) > 0:
            properties['color'] = color
        self.__loop.call_soon(self.__callback, start_time, properties)

    @asyncio.coroutine
    def run(self):
        if self.isRunning():
            raise Exception('Blockupdate is already running')

        self.__aborted = False
        start_time = time.time()
        cmd = self.__properties['_command']
        if cmd is None:
            self.__return(start_time)
            return

        self.__process = yield from asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=None,
            env=self.__env,
            loop=self.__loop)
        #e = asyncio.Event(loop=self.__loop)
        #p = self.__loop.create_task(
        #    asyncio.create_subprocess_shell(
        #        cmd,
        #        stdout=asyncio.subprocess.PIPE,
        #        stderr=None,
        #        env=self.__env,
        #        loop=self.__loop)
        #)
        #p.add_done_callback(lambda _:e.set())
        #print('wait')
        #e.wait()
        #print('awake')
        #print(p.result())
        #self.__process = p.result()

        #print('grrr')

        try:
            #res, _ = self.__loop.run_until_complete(
            #    asyncio.wait_for(self.__process.communicate(),
            #                     self.__timeout,
            #                     loop=self.__loop))
            res, _ = yield from asyncio.wait_for(
                self.__process.communicate(),
                self.__timeout,
                loop=self.__loop)
        except asyncio.TimeoutError:
            # log timeout
            self.abort()
            return

        lines = res.decode().splitlines()
        lines.append('')
        lines.append('')
        lines.append('')

        self.__return(start_time, lines[0], lines[1], lines[2])

    def isRunning(self):
        if self.__process is None:
            return None

        return self.__process.returncode is None

    def abort(self):
        if self.isRunning():
            self.__aborted = True
            self.__process.terminate()
from .BlockProperties import BlockProperties


class BlockProvider():

    def __init__(self, server, name):
        self.__server = server

        self.__properties = BlockProperties(name)

        self.block = self.__properties

        self.__updates = []

        self.__last_update = 0

        self.__aborted = False

        self.__scheduler = self.__server.get_loop().call_soon(self.__schedule)

        #self.request_update()

    def reconfigure(self, configParser):
        if self.__properties.read(configParser):
            self.abort()
            self.__server.get_loop().call_soon(self.request_update)

    def abort(self):
        for update in self.__updates:
            update.abort()

        self.__updates = []

    def request_update(self):
        update = None
        for u in self.__updates:
            if not u.isRunning():
                update = u
                break

        if update is None:
            update = BlockUpdate(self.__server.get_loop(), self.__properties.copy(), self._update)
            self.__updates.append(update)

        # TODO: make this a direct call, block any other update requests and then start a task for the actual work
        #       with this we got some "Blockupdate is already running" Exceptions
        self.__server.get_loop().create_task(update.run())

    def __nextRun(self, t):
        # TODO: use default interval istead of hardcoded 5
        interval = 5
        try:
            interval = float(self.__properties['_interval'])
        except:
            pass
        t += interval

        if 604800 % interval == 0:
            t = t - t % interval

        t = t - time.time() + self.__server.get_loop().time()

        return t

    def __schedule(self):
        if self.__aborted:
            return

        t = self.__nextRun(time.time())
        self.request_update()

        self.__scheduler = self.__server.get_loop().call_at(t, self.__schedule)

    def _update(self, start_time, properties):
        if start_time > self.__last_update:
            self.__last_update = start_time
            self.block = properties
            self.__server.requireUpdate(self)
