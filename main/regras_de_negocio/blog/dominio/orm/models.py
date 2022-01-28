from datetime import datetime
from main import database

class Postagens(database.Model):

    __tablename__ = 'posts'

    id = database.Column(database.Integer, primary_key=True)
    corpo = database.Column(database.Text)
    hora_postagem = database.Column(database.DateTime, index=True, default=datetime.now)
    autor_id = database.Column(database.Integer, database.ForeignKey('usuarios.id'))