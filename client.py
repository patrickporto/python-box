# encoding: utf-8
import os
from argparse import ArgumentParser
from websocket import Client


def start_server(path):
    try:
        ws = Client(url='ws://localhost:9000/', path=path, protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('directory', metavar='DIRETÓRIO', type=str,
                        help='diretório para sincronização')
    args = parser.parse_args()
    if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
        parser.error("diretório para sincronização inexistente")
    start_server(args.directory)
