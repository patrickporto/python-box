# encoding: utf-8
import os
from argparse import ArgumentParser
from websocket import Client


def start_server(path, host, port):
    try:
        ws = Client(
            url='ws://{host}:{port}/'.format(host=host, port=port),
            path=path,
            protocols=['http-only', 'chat'],
        )
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('directory', metavar='DIRETÓRIO', type=str,
                        help='diretório para sincronização')
    parser.add_argument('--host', metavar='SERVIDOR', type=str,
                        help='endereço do servidor (padrão: localhost)',
                        default='localhost')
    parser.add_argument('--port', metavar='PORTA', type=str,
                        help='endereço do servidor (padrão: 9000)',
                        default='9000')
    args = parser.parse_args()
    if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
        parser.error("diretório para sincronização inexistente")
    start_server(args.directory, args.host, args.port)
