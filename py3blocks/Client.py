from .ClientConnectionHandler import ClientConnectionHandler

import asyncio


class Client:
    def __init__(self, loop, address, port):
        self.__loop = loop
        self.__address = address
        self.__port = port
        self.__client = None

    def run(self):
        print('{"version":1,"click_events":true}')
        print('[[]')
        #self.__loop.call_soon(self.connect)
        self.__loop.run_until_complete(self.connect())

    async def connect(self):
        try:
            # reader, writer = await asyncio.open_connection(port=self.__port, server_hostname=self.__address)
            self.__client = await self.__loop.create_connection(lambda: ClientConnectionHandler(self),
                                                                port=self.__port,
                                                                server_hostname=self.__address)
        except OSError as e:
            # TODO: Log connection error
            await asyncio.sleep(15)
            self.__loop.create_task(self.connect())
            return

        #print(reader,writer)

    def close(self):
        pass

    async def wait_closed(self):
        pass

    def connection_lost(self, transport, exc):
        # TODO: log exc
        # TODO: restart conection
        if transport is not None:
            transport.close()
        self.__loop.create_task(self.connect())
