class Produto(database.Model):
    __tablename__ = 'produtos'

    id = database.Column(database.Integer, primary_key=True)
    referencia = database.Column(database.String(255), unique=True)
    identificador = database.Column(database.String(255), unique=True)
    quantidade_disponivel = database.Column(database.Integer, nullable=False)
    pedidos = database.relationship('Pedido', backref='produto')

    def __repr__(self) -> str:
        return '<Produto %r>' % self.referencia


class Pedido(database.Model):
    __tablename__ = 'pedido'

    id = database.Column(database.Integer, primary_key=True)
    identificador = database.Column(database.String(255), unique=True)
    quantidade = database.Column(database.Integer, nullable=False)
    id_pedido = database.Column(database.String(255), unique=True)
    id_produto = database.Column(database.Integer, database.ForeignKey('produtos.id'))

    def __repr__(self) -> str:
        return '<Pedido %r>' % self.id_pedido