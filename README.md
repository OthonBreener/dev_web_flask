## Iniciando o sistema

* Váriavel de ambiente necessária para o comando
flask run, encontre o nome do scprit python que
contém a instância da aplicação FLASK().

```
export FLASK_APP=main/app.py
```

* Váriavel de ambiente necessária para iniciar o modo
de depuração:

```
export FLASK_DEBUG=1
```

## Rodando os tests:

* Rodando todos os testes:
  
python -m unittest

*  Rodando um arquivo especifico: 
python -m unittest tests/unit/test_user_model.py

## Migração do banco de dados

* flask db migrate -m "Descrição"
* flask db upgrade

## Inserindo as regras de acesso no banco de dados

* from main.regras_de_negocio.governancia.models import RegrasDeAcesso as Regras
* Regras.inserir_regras()
* adm = Regras.query.filter_by(name='administrador').first()
* user = Usuario.query.filter_by(user_name='Othon').fisrt()
* user.regra = Regras.query.filter_by(name='administrador').fisrt()
* db.session.commit()
