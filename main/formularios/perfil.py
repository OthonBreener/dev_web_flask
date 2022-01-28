from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, ValidationError, FileField
from wtforms.validators import Length, DataRequired, Regexp, Email

from main.regras_de_negocio.governancia.models import RegrasDeAcesso
from main.regras_de_negocio.usuarios.dominio.orm.models import Usuario


class EditarPerfil(FlaskForm):

    name = StringField('Nome completo', validators=[Length(0, 64)])
    location = StringField('Localização', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mim')
    imagem = FileField('Foto')
    submit = SubmitField('Enviar')


class AdmEditPerfil(FlaskForm):

    email = StringField('Email', 
        validators=[DataRequired(), Length(1, 64), Email()])
    
    user_name = StringField('Nome', validators=[
        DataRequired(), Length(1, 64),
        Regexp(
            '^[A-Za-z][A-Za-z0-9_.]*$', 0,
            'O nome do usuário deve conter apenas letras, números, pontos ou underline.'
        )
    ])

    confirmed = BooleanField('Confirmado')
    regras = SelectField('Regra de Acesso', coerce=int)
    name = StringField('Nome completo', validators=[Length(0, 64)])
    location = StringField('Localização', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mim')
    submit = SubmitField('Enviar')
    imagem = FileField('Foto')

    def __init__(self, user, *args, **kwargs):
        super(AdmEditPerfil, self).__init__(*args, **kwargs)
        self.regras.choices = [
            (regra.id, regra.name) 
            for regra in RegrasDeAcesso.query.order_by(RegrasDeAcesso.name).all()]
    
        self.user = user


    def validate_email(self, field):
        if field.data != self.user.email and Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('Email já cadastrado')
    
    
    def validate_user_name(self, field):
        if field.data != self.user.user_name and Usuario.query.filter_by(user_name=field.data).first():
            raise ValidationError('Nome de usuário já cadastrado')