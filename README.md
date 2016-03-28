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
Executar servidor de sincronização.
```shell
python server start pasta/de/armazenamento --host 0.0.0.0 --port 9000
```

##  Cliente ##
Executar cliente para sincronização.
```shell
python client minha/pasta/com/arquivos --host 0.0.0.0 --port 9000
```
