# encoding: utf-8
import os
from argparse import ArgumentParser
from websocket_client import start_server, login


parser = ArgumentParser()
subparsers = parser.add_subparsers()
parser_startsync = subparsers.add_parser('startsync', help='sincroniza pasta com o servidor')
parser_startsync.add_argument('directory', metavar='DIRETÓRIO', type=str,
                              help='diretório para sincronização')
parser_startsync.add_argument('--host', metavar='SERVIDOR', type=str,
                              help='endereço do servidor (padrão: localhost)',
                              default='localhost')
parser_startsync.add_argument('--port', metavar='PORTA', type=int,
                              help='porta do servidor (padrão: 9000)',
                              default='9000')
parser_startsync.set_defaults(cmd='startsync')

parser_login = subparsers.add_parser('login', help='autentica no servidor')
parser_login.add_argument('username', metavar='USUÁRIO', type=str,
                          help='nome de usuário')
parser_login.add_argument('password', metavar='SENHA', type=str,
                          help='senha do usuário')
parser_login.add_argument('--host', metavar='SERVIDOR', type=str,
                          help='endereço do servidor (padrão: localhost)',
                          default='localhost')
parser_login.add_argument('--port', metavar='PORTA', type=int,
                          help='porta do servidor (padrão: 9000)',
                          default='9000')
parser_login.set_defaults(cmd='login')

args = parser.parse_args()

if args.cmd == 'startsync':
    if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
        parser.error("diretório para sincronização inexistente")
    start_server(args.directory, args.host, args.port)
elif args.cmd == 'login':
    login(args.username, args.password, args.host, args.port)
