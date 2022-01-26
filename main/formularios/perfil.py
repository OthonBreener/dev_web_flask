from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class EditarPerfil(FlaskForm):

    name = StringField('Nome completo', validators=[Length(0, 64)])
    location = StringField('Localização', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mim')
    submit = SubmitField('Enviar')