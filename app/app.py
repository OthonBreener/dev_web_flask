from os import getenv, path
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from formularios.models import Usuario as User


basedir = path.abspath(path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)


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


class Usuario(database.Model):

    __tablename__ = 'usuarios'

    id = database.Column(database.Integer, primary_key=True)
    user_name = database.Column(database.String(64), unique=True, index=True)

    def __repr__(self) -> str:
        return '<Usuario %r>' % self.user_name


bootsprap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def user():
    form = User()
    if form.validate_on_submit():
        session['name'] = form.name
        return redirect(url_for('user'))

    return render_template(
        'pagina_inicial/user.html',
        form=form,
        name=session.get('name'))

#rotas de erro

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500
