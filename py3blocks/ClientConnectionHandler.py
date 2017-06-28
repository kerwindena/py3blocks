import asyncio
from .JSONEncoder import JSONEncoder

import json
from sys import stdout

class ClientConnectionHandler(asyncio.Protocol):

    def __init__(self, client):
        self.__client = client
        self.__transport = None

    def connection_made(self, transport):
        self.__transport = transport
        # TODO: Log print('Connected to {}'.format(
        #    transport.get_extra_info('socket').getsockname()))

    def connection_lost(self, exc):
        self.__client.connection_lost(self.__transport, exc)

    def data_received(self, data):
        lines = data.decode().split('\n')
        if len(lines) > 1:
            for line in lines:
                if line.startswith(',['):
                    print(line)
                    stdout.flush()
