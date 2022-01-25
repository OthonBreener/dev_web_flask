from gettext import find
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
    
    @staticmethod
    def inserir_regras():
        regras = {
            'usuario':[Permissions.ADICIONAR_AO_CARRINHO, Permissions.FINALIZAR_COMPRA],
            'administrador':[
                Permissions.VISUALIZAR_USUARIOS_CADASTRADOS,
                Permissions.REMOVER_USUARIO_CADASTRADO,
                Permissions.ADMINISTRADOR
            ]
        }

        regra_default = 'usuario'
        for regra in regras:

            find_regra = RegrasDeAcesso.query.filter_by(name=regra).first()
            if find_regra is None:
                find_regra = RegrasDeAcesso(name=regra)
            
            find_regra.reset_permissions()

            for permission in regras[regra]:
                find_regra.add_permission(permission)
            
            find_regra.default = (find_regra.name == regra_default)
            database.session.add(find_regra)
            
        database.session.commit()


class Permissions:
    ADICIONAR_AO_CARRINHO=1
    FINALIZAR_COMPRA=2
    VISUALIZAR_USUARIOS_CADASTRADOS=4
    REMOVER_USUARIO_CADASTRADO=8
    ADMINISTRADOR=16

