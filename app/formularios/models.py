from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField
)
from wtforms.validators import DataRequired


class Usuario(FlaskForm):
    name = StringField('Usuário: ', validators=[DataRequired()])
    senha = PasswordField('Senha: ', validators=[DataRequired()])
    submit = SubmitField('Entrar')
