from email.policy import default
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from main import login_manager, database
from main.regras_de_negocio.governancia.models import Permissions, RegrasDeAcesso

class Usuario(UserMixin, database.Model):

    __tablename__ = 'usuarios'

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(64), unique=True, index=True)
    user_name = database.Column(database.String(64), unique=True, index=True)
    password_hash = database.Column(database.String(128))
    confirmed = database.Column(database.Boolean, default=False)

    def __repr__(self) -> str:
        return '<Usuario %r>' % self.user_name


    def __init__(self, **kwargs) -> None:
        super(Usuario, self).__init__(**kwargs)
        if self.RegrasDeAcesso is None:
            if self.email == current_app.config['ADMIN']:
                self.RegrasDeAcesso = RegrasDeAcesso.query.filter_by(
                    name='administrador').first()
            
            if self.RegrasDeAcesso is None:
                self.RegrasDeAcesso = RegrasDeAcesso.query.filter_by(
                    default=True).first()
    

    def can(self, permission):
        return (self.RegrasDeAcesso is not None and 
                self.RegrasDeAcesso.has_permission(permission))
    

    def is_administrador(self):
        return self.can(Permissions.ADMINISTRADOR)


    @property
    def password(self):
        raise AttributeError("A senha não é um atributo legível")
    

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def gerador_de_token_de_confirmacao(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')
    

    def confirmar_conta(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            dados = s.loads(token.encode('utf-8'))
        except:
            return False

        if dados.get('confirm') != self.id:
            return False
        
        self.confirm = True
        database.session.add(self)
        return True


class UsuarioAnonimo(AnonymousUserMixin):

    def can(self, permission):
        return False
    
    def is_administrador(self):
        False


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

login_manager.anonymous_user = UsuarioAnonimo