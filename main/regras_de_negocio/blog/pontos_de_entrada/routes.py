from sys import prefix
from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user

from main import database
from main.formularios.posts import PostagensForm
from main.regras_de_negocio.blog.dominio.orm.models import Postagens
from main.regras_de_negocio.governancia.models import Permissions

bp_posts = Blueprint('bp_posts', __name__, url_prefix='/post')


@bp_posts.route('/', methods=['GET', 'POST'])
def index():
    form = PostagensForm()
    if current_user.can(Permissions.ESCREVER_POSTAGENS) and form.validate_on_submit():
        postagem = Postagens(
            corpo = form.corpo.data,
            autor=current_user._get_current_object()
        )
        database.session.add(postagem)
        database.session.commit()
        return redirect(url_for('bp_posts.index')) 
    
    postagens = Postagens.query.order_by(Postagens.hora_postagem.desc()).all()
    return render_template('pagina_inicial/index.html', posts=postagens, form=form)


@bp_posts.app_context_processor
def inject_permissions():
    """
    Processador de contexto deixa uma variavel disponível a todos
    os templates durante a renderização.
    """
    return dict(Permissions=Permissions)

def configure(app):
    app.register_blueprint(bp_posts)