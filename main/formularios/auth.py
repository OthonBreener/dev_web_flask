from flask_wtf import FlaskForm
from pyparsing import Regex
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from main.regras_de_negocio.usuarios.models import Usuario


class LoginForm(FlaskForm):

    email = StringField('Email', 
        validators=[DataRequired(), Length(1, 64), Email()])
    
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_de_mim = BooleanField('Lembrar de mim?')
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):

    email = StringField('Email', 
        validators=[DataRequired(), Length(1, 64), Email()])
    
    user_name = StringField('Nome', validators=[
        DataRequired(), Length(1, 64),
        Regexp(
            '^[A-Za-z][A-Za-z0-9_.]*$', 0,
            'O nome do usuário deve conter apenas letras, números, pontos ou underline.'
        )
    ])

    password = PasswordField('Senha', validators=[
        DataRequired(), 
        EqualTo('password2', message='As senhas devem ser iguais!')
        ]
    )

    password2 = PasswordField('Confirmar senha', validators=[DataRequired()])

    submit = SubmitField('Registrar')


    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('Email já cadastrado')
    
    def validate_user_name(self, field):
        if Usuario.query.filter_by(user_name=field.data).first():
            raise ValidationError('Nome de usuário já cadastrado')