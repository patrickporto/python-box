# encoding: utf-8
import os
from argparse import ArgumentParser
from websocket_server import start_server


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('directory', metavar='DIRETÓRIO', type=str,
                        help='diretório para hospedagem e sincronização')
    parser.add_argument('--host', metavar='SERVIDOR', type=str,
                        help='endereço para execução (padrão: 0.0.0.0)',
                        default='0.0.0.0')
    parser.add_argument('--port', metavar='PORTA', type=int,
                        help='porta para execução (padrão: 9000)',
                        default='9000')
    args = parser.parse_args()
    if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
        parser.error("diretório para sincronização inexistente")
    start_server(args.directory, args.host, args.port)
