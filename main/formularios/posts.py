from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostagensForm(FlaskForm):
    corpo = TextAreaField('O que você está pensando?', validators=[DataRequired()])
    submit = SubmitField('Enviar')