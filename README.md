
# Vehicles

Um projeto para testar minhas habilidades.


## Funcionalidades

- Autenticação com JWT
- Cadastro, deleção, edição e leitura de veículos
- Rotas públicas
- Rotas privadas
- Persistência de dados utilizando PostgreSQL
- Upload de imagens através do imageKit
- Deleção de imagens

## Instalação

Clone o repositório

```bash
git clone git@github.com:Fernando12mais/vehicles.git
```



Crie uma conta no imageKit acessando [imageKit](https://imagekit.io/registration/)



## Variáveis de Ambiente

Na pasta raiz do projeto crie um arquivo .env

Acesse seu dashboard no imageKit [dashboard](https://imagekit.io/dashboard/developer/api-keys)

Dentro do arquivo .env, crie as seguintes variáveis e cole os secrets de sua conta



`IMAGE_KIT_PRIVATE_KEY`="aqui vai sua private key"

`IMAGE_KIT_PUBLIC_KEY` ="aqui vai sua public key"

`IMAGE_KIT_URL_ENDPOINT` ="aqui vai sua url-endpoint"


## Instalando dependencias

Este projeto usa docker containers, para rodar o projeto é preciso ter o docker instalado

### docker
Siga a documentação descrita aqui [docker](https://docs.docker.com/get-docker/)

### docker-compose
Siga a documentação descrita aqui [ docker-compose](https://docs.docker.com/compose/install/)









## Rodando o projeto
Vá para a pasta raiz do projeto e abra o terminal, rode o seguinte comando:

```bash
docker-compose up
```

Se você instalou a versão docker desktop é só clicar no ícone de play dos containers e não precisa do comando acima.
## Acessando a API

A API está rodando na porta 8000, para acessar basta ir para http://localhost:8000/docs
