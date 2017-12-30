# RedisMySQLPythonWorker - Redis + MySQL + Python

  - A base migrada deverá possibilitar as seguintes consultas:

    - Consultar o nome do usuário e retornar os pedidos deste usuário (question1.py).
    - Consultar o estado e retornar os usuários deste estado (question2.py).
    - Consultar o produto e retornar os dados dos produtos (question3.py).
    - Consultar pelo pedido e retornar os dados do pedido (question4.py).
    - Consultar o usuário e retornar os dados do usuário (question5.py).
    - Consultar cidade e retornar usuários desta cidade (question6.py).
    - Consultar o estado e retornar os dados de todos os logradouros deste estado (question7.py).
    - Cadastrar um novo usuário (question8.py).
    - Inserir um pedido para determinado usuário (question8.py).

# Requisitos necessário para funcionamento da aplicação:

```
pip install redis
```

```
pip install oursql
```

Adicionar suas próprias informações, por padrão o MySQL e o Redis utilizam localhost, root para o administrador, e em seguida a base que você deseja acessar. **Quando chamar a função, passar o cursor do mysql e do redis.**
