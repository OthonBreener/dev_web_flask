from main import database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from main import login_manager

class Usuario(UserMixin, database.Model):

    __tablename__ = 'usuarios'

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(64), unique=True, index=True)
    user_name = database.Column(database.String(64), unique=True, index=True)
    password_hash = database.Column(database.String(128))

    def __repr__(self) -> str:
        return '<Usuario %r>' % self.user_name


    @property
    def password(self):
        raise AttributeError("A senha não é um atributo legível")
    

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))