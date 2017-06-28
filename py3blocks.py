#!/usr/bin/env python3

import asyncio
import argparse

import py3blocks


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate content for the i3status bar.')

    action = parser.add_mutually_exclusive_group()
    action.add_argument('--server', action='store_true')
    action.add_argument('--i3bar', action='store_true')

    parser.add_argument('--address', '-a')
    parser.add_argument('--port', '-p',
                        type=int,
                        required=True)

    parser.add_argument('--config', '-c')

    return parser.parse_args()


def main():
    args = parse_args()

    loop = asyncio.get_event_loop()

    if args.server:
        sock = py3blocks.Networking.create_server_sock(
            (args.address, args.port))
        server = py3blocks.Server(loop, sock, [args.config])
        server.run()

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        sock.close()

    if args.i3bar:
        client = py3blocks.Client(loop, args.address, args.port)
        client.run()

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        client.close()
        loop.run_until_complete(client.wait_closed())

    loop.close()


if __name__ == '__main__':
    main()
