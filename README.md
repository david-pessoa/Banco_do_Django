# Banco do Django

## Descrição
Essa aplicação simples feita em Django, tem o intuito

Este projeto tem apenas o intuito de ser um estudo para meu aprimoramento no Django.

## Como instalar
Caso deseje instalar a aplicação, antes é necessário possuir instalados em sua máquina:
* <a href="https://www.python.org/downloads/">Python 3.12 ou superior</a>
* <a href="https://www.postgresql.org/download/">PostgresSQL</a>

### 1) Clone o repositório e entre no diretório Fusion
```sh
git clone https://github.com/david-pessoa/Fusion.git
cd Fusion
```

### 2) Crie um ambiente virtual e ative-o
```sh
python3 -m venv venv
```

Se estiver no MacOS ou Linux, ative o venv executando:
```sh
source venv/bin/activate
```

Se estiver no Windows, ative o venv executando:
```sh
source venv/Scripts/activate
```

### 3) Instale as bibliotecas necessárias
```sh
pip install -r requirements.txt
```

### 4) Crie o banco de dados em SQL com PostgreSQL
Agora, será necessário criar o banco de dados. Para isso, acesse o postgres pelo usuário `postgres`
```sh
sudo -i -u postgres
# Acesso ao postgres
psql
```

Crie o banco, e um usuário com privilégios
```sh
create database nome_banco;
create user nome_usuario with encrypted password 'senha_dentro_das_aspas_simples';
grant all privileges on database nome_banco to nome_usuario;
\q
```

### 5) Crie um arquivo .env com as informações do projeto
Crie um arquivo .env e escreva em seu interior sua própria `SECRET_KEY` e as informações do banco de dados assim:
```
SECRET_KEY='sua_secret_key'

#DATABASE
DB_NAME='nome do seu banco'
DB_USER='seu usuario'
DB_PASSWORD='sua senha'
DB_HOST='localhost' #Digite onde irá rodar
```
para gerar uma `SECRET_KEY`, digite no terminal:
```sh
python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 6) Faça a migração dos dados para o banco e rode a aplicação
```sh
python manage.py migrate
python manage.py runserver
```

Pronto, agora você já pode acessar a aplicação Django! :) Não se esqueça de verificar se a aplicação está no modo Produção ou Desenvolvimento.
