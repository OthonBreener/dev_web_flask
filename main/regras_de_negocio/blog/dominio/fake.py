from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker

from main import database
from main.regras_de_negocio.blog.dominio.orm.models import Postagens
from main.regras_de_negocio.usuarios.dominio.orm.models import Usuario


def usuarios_fake(contador = 100):

    fake = Faker()
    i= 0
    while i < contador:
        user = Usuario(
            email = fake.email(),
            user_name = fake.user_name(),
            password = 'senha',
            confirmed = True,
            name = fake.name(), 
            location = fake.city(),
            about_me = fake.text(),
            membro_desde = fake.past_date()
        )
        database.session.add(user)
        try:
            database.session.commit()
            i += 1
        except IntegrityError:
            database.session.rollback()


def postagens_fake(contador=100):

    fake = Faker()
    user_count = Usuario.query.count()
    for i in range(contador):
        user = Usuario.query.offset(randint(0, user_count -1)).first()
        posts = Postagens(
            corpo = fake.text(),
            hora_postagem = fake.past_date(),
            autor=user
        )
        database.session.add(posts)
    database.session.commit()


