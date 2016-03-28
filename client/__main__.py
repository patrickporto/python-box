# encoding: utf-8
import os
from argparse import ArgumentParser
from websocket_client import start_server


parser = ArgumentParser()
parser.add_argument('directory', metavar='DIRETÓRIO', type=str,
                    help='diretório para sincronização')
parser.add_argument('--host', metavar='SERVIDOR', type=str,
                    help='endereço do servidor (padrão: localhost)',
                    default='localhost')
parser.add_argument('--port', metavar='PORTA', type=int,
                    help='porta do servidor (padrão: 9000)',
                    default='9000')
args = parser.parse_args()
if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
    parser.error("diretório para sincronização inexistente")
start_server(args.directory, args.host, args.port)
