# jujuba-backend

## Acesso ao Swagger
Deploy realizado no heroku:

**[jujuba-api](https://jujuba-api.herokuapp.com/docs#)**

### VirtualEnv
- Criar um [virtualenv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

* Se não tiver esse pacote instlado, faça a instalação rodando o comando:
```
pip install virtualenv
```

- E crie seu virtualenv com:
```
venv python3 -m venv 'qualquernome'
```

- Por ultimo ative seu virtualenv com:
```
linux:

source 'qualquernome'/bin/activate
```
```
windows:

.\'qualquernome'\Scripts\activate
```

Também é possível activer indo de pasta em pasta:
```
cd 'qualquernome'

cd Scripts/

. activate
```

Fazendo dessa forma não esqueça de voltar para a pasta raiz utilizando o cd ..

- Para desativar basta digitar:
```
deactivate
```

### Dependencias
- Instalar as [dependencias](https://stackoverflow.com/questions/7225900/how-can-i-install-packages-using-pip-according-to-the-requirements-txt-file-from)

```
pip install -r requirements.txt
```

### Credenciais Para Acessar no PostgreSQL
- Crie um arquivo .env na raiz do projeto

- Dentro desse arquivo coloque o seguinte conteúdo:
```
DATABASE_URL='postgresql://user:password@port/name_db'
```

### Rodar Aplicação Local
- Utilizar o comando:
```
uvicorn main:app --reload
```
- Acessar o Swagger:
```
http://localhost:8000/docs
```
- Ou aperte F5 que já rodará aplicação com o debbuger

### Débitos Tecnicos
[ ] Adicionar token de autenticação para o login  
[ ] Realizar testes unitários  
[ ] Adicionar validações (letra maiuscula/minuscula, espaços...)  
