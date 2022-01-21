from main import database

class Usuario(database.Model):

    __tablename__ = 'usuarios'

    id = database.Column(database.Integer, primary_key=True)
    user_name = database.Column(database.String(64), unique=True, index=True)

    def __repr__(self) -> str:
        return '<Usuario %r>' % self.user_name