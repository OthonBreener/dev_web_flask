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
