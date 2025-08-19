# Judge API

## Setup
# **Aqui é a aba onde vamos seguir os passos para rodar o projeto!**

## **Execute comando a comando**

1. Crie um ambiente virtual

```
python3 -m venv venv
```

1. Ative ele

```
source venv/bin/activate
```

1. Dentro do ambiente, instale o **poetry** por meio do **pip install**

```
pip install poetry
```

1. A partir do poetry, instale as dependencias automaticamente que estão listadas em **pyproject.toml**

```
poetry install
```

## Após isso, inicialize os serviços do docker:

```
docker-compose up -d --build
```

## Acesse:

```text
http://127.0.0.1:8000/docs#/
```

## Para gerar o token de autenticação:

1. Acesse o site: [https://10015.io/tools/jwt-encoder-decoder](https://10015.io/tools/jwt-encoder-decoder "smartCard-inline")
2. No campo Signing Key:

```
sua-chave-secreta
```

1. Clique no botão **Add Claims +**
2. No campo **Subject (sub)**:

```
api_externa
```

1. Clique em **Encode**
2. Clique em **Copy JWT**