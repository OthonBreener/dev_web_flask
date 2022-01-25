from main import database


class RegrasDeAcesso(database.Model):

    __tablename__ = 'regras'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), unique=True)
    default = database.Column(database.Boolean, default=False, index=True)
    permissions = database.Column(database.Integer)
    usuarios = database.relationship('Usuario', backref='RegrasDeAcesso', lazy='dynamic')


    def __init__(self, **kwargs) -> None:
        super(RegrasDeAcesso, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    def has_permission(self, param):
        return self.permissions & param == param


    def add_permission(self, param):
        if not self.has_permission():
            self.permissions += param


    def remove_permission(self, param):
        if self.has_permission(param):
            self.permissions -= param


    def reset_permissions(self):
        self.permissions = 0


class Permissions:
    ADICIONAR_AO_CARRINHO=1
    FINALIZAR_COMPRA=2
    ADMINISTRADOR=4

