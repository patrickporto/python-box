# encoding: utf-8
from __future__ import print_function
import os
from argparse import ArgumentParser
from websocket_server import start_server
from db import database
from models import __all__, User


parser = ArgumentParser()
subparsers = parser.add_subparsers()
parser_start = subparsers.add_parser('start', help='executar servidor de sincronização')
parser_start.set_defaults(cmd='start')
parser_start.add_argument('directory', metavar='DIRETÓRIO', type=str,
                          help='diretório para hospedagem e sincronização')
parser_start.add_argument('--host', metavar='SERVIDOR', type=str,
                          help='endereço para execução (padrão: 0.0.0.0)',
                          default='0.0.0.0')
parser_start.add_argument('--port', metavar='PORTA', type=int,
                          help='porta para execução (padrão: 9000)',
                          default='9000')
parser_syncdb = subparsers.add_parser('syncdb', help='cria tabelas do banco de dados')
parser_syncdb.set_defaults(cmd='syncdb')
parser_createuser = subparsers.add_parser('createuser', help='cria usuário')
parser_createuser.add_argument('username', metavar='USUÁRIO', type=str,
                               help='nome de usuário')
parser_createuser.add_argument('password', metavar='SENHA', type=str,
                               help='senha do usuário')
parser_createuser.set_defaults(cmd='createuser')
args = parser.parse_args()

if args.cmd == 'start':
    if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
        parser.error("diretório para sincronização inexistente")
    start_server(args.directory, args.host, args.port)
elif args.cmd == 'syncdb':
    database.connect()
    print('Creating tables ...')
    database.create_tables(__all__)
    print('Installing custom SQL ...')
    print('Installing indexes ...')
    print('Installed 0 object(s) from 0 fixture(s)')
elif args.cmd == 'createuser':
    User.create(
        username=args.username,
        password=args.password,
    )
