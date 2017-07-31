import asyncio
from .JSONEncoder import JSONEncoder

import asyncio
import json


class ConnectionHandler(asyncio.Protocol):

    def __init__(self, server):
        self.__server = server
        self.__blocks = server._Server__blocks
        self.__update = None

    def connection_made(self, transport):
        self.transport = transport
        self.__server.add_connection(self)
        print('Connection established with {}'.format(self.transport.get_extra_info('peername')))
        self.writeln('{"version":1,"click_events":true}')
        self.writeln('[[]')
        self.require_update()

    def connection_lost(self, exc):
        self.__server.remove_connection(self)
        print('Connection teared down with {}'.format(self.transport.get_extra_info('peername')))

    def require_update(self, block=None):
        if self.__update is not None:
            return

        if block is None or block in self.__blocks.values():
            self.__update = self.__server.get_loop().create_task(self.update())

    @asyncio.coroutine
    def update(self):
        yield from asyncio.sleep(0.08)
        self.__update = None
        self.writeln(',' + json.dumps(self, cls=JSONEncoder))

    def data_received(self, data):
        print(data)

    def has_block(self, block):
        return block in self.__blocks.values()

    def get_blocks(self):
        return self.__blocks.copy()

    def writeln(self, data):
        self.write(data)
        self.write(b'\n')

    def write(self, data):
        if type(data) == str:
            data = data.encode()

        self.transport.write(data)
