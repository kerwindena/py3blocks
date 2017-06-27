# from .Block import Block
from .BlockProvider import BlockProvider
from .ConfigParser import ConfigParser
from .ConnectionHandler import ConnectionHandler

import os

class Server():

    def __init__(self, loop, sock):
        self.__loop = loop
        self.__sock = sock
        self.__connections = []
        self.__blocks = {}
        self.__configParser = ConfigParser(strict=False)

    def run(self):
        self.readConfig()

        coro = self.__loop.create_server(lambda: ConnectionHandler(self), sock=self.__sock)
        self.__server = self.__loop.run_until_complete(coro)

        print('Serving on {}'.format(self.__sock.getsockname()))

    def update_config(self):
        self.__blocks

    def get_loop(self):
        return self.__loop

    def get_connections(self):
        for connection in self.__connections:
            yield connection

    def add_connection(self, connection):
        self.__connections.append(connection)

    def remove_connection(self, connection):
        self.__connections.remove(connection)

    def reschedule(self):
        pass

    def readConfig(self):
        self.__configParser.read(['i3blocks.conf', os.path.expanduser('~/.i3blocks.conf')])

        sections = self.__configParser.sections()

        blocks = [section for section in sections if not section.startswith('bar/')]
        bars = [section for section in sections if section.startswith('bar/')]

        # for block in blocks:
        #     if block not in self.__blocks:
        #         self.__blocks[block] = Block(self, block)

        #     self.__blocks[block].reconfigure(self.__configParser, block)
        for block in blocks:
            if block not in self.__blocks:
                self.__blocks[block] = BlockProvider(self, block)

                self.__blocks[block].reconfigure(self.__configParser)

    def requireUpdate(self, block=None):
        for connection in self.__connections:
            connection.require_update(block)

    def close(self):
        self.__server.close()
        for block in list(self.__blocks):
            # self.__blocks[block].cancel()
            self.__blocks[block].abort()
            del self.__blocks[block]

    async def wait_closed(self):
        await self.__server.wait_closed()
