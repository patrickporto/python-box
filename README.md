# python-box
Tenha acesso direto à uma pasta do servidor através de uma pasta no disco rígido do seu computador.

## Pré-requisitos ##
* Ubuntu 14.04 ou superior.
* Python 2.7

## Dependências ##
> O uso de **virtualenv** e **virtualenvwrapper** é altamente recomendável.  
> Veja mais:  
> 1. https://virtualenv.pypa.io/en/latest/
> 2. https://virtualenvwrapper.readthedocs.org/en/latest/

Instale as dependências tanto do **cliente** quanto do **server** através do seguinte comando:
```shell
pip install -r requirements.txt
```

## Servidor ##
```shell
usando: server [-h] [--host SERVIDOR] [--port PORTA] DIRETÓRIO

argumentos posicionais:
  DIRETÓRIO       diretório para hospedagem e sincronização

  argumentos opcionais:
  -h, --help       apenas exibe esta ajuda
  --host SERVIDOR  endereço para execução (padrão: 0.0.0.0)
  --port PORTA     porta para execução (padrão: 9000)

```

##  Cliente ##
```shell
usando: client [-h] [--host SERVIDOR] [--port PORTA] DIRETÓRIO

argumentos posicionais:
  DIRETÓRIO       diretório para sincronização

argumentos opcionais:
  -h, --help       apenas exibe esta ajuda
  --host SERVIDOR  endereço do servidor (padrão: localhost)
  --port PORTA     porta do servidor (padrão: 9000)
```
