from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from main.formularios.perfil import AdmEditPerfil, EditarPerfil
from main.regras_de_negocio.governancia.models import Permissions, RegrasDeAcesso
from main.regras_de_negocio.usuarios.decoradores.decorador import admin_required, permission_required
from main.regras_de_negocio.usuarios.models import Usuario
from main.formularios.auth import LoginForm, RegistrationForm
from main import database


bp = Blueprint('bp', __name__, url_prefix='/user')


@bp.route('/')
def index():
    return render_template('pagina_inicial/index.html')


@bp.route('/<user_name>')
def perfil_de_usuario(user_name):
    user = Usuario.query.filter_by(user_name=user_name).first_or_404()
    
    return render_template(
            'usuarios/perfil.html', 
            user=user,
            imagem=url_for('static', filename='imagens/' + user.imagem)
        )


@bp.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():

    form = EditarPerfil()
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        
        imagem = form.imagem.data
        formato = imagem.mimetype.split('/')[-1]
        caminho = '/home/othonbreener/Documentos/EstudosPython/dev_web_flask/main/static/imagens/'
        name_image = caminho + 'user_' + current_user.user_name + '.' + formato

        imagem.save(name_image)
        current_user.imagem = 'user_' + current_user.user_name + '.' + formato

        database.session.add(current_user._get_current_object())
        database.session.commit()
        flash('Seu perfil foi atualizado com sucesso!')
        
        return redirect(url_for('bp.perfil_de_usuario', user_name=current_user.user_name))

    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me

    return render_template('usuarios/editar_perfil.html', form=form)


@bp.route('/editar-perfil/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_perfil_admin(id):

    user = Usuario.query.get_or_404(id)
    form = AdmEditPerfil(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.user_name = form.user_name.data
        user.confirmed = form.confirmed.data
        user.regra = RegrasDeAcesso.query.get(form.regras.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        
        database.session.add(user)
        database.session.commit()
        flash('Perfil atualizado com sucesso!')

        return redirect(url_for('bp.perfil_de_usuario', user_name=user.user_name))
    
    form.email.data = user.email
    form.user_name.data = user.user_name
    form.confirmed.data = user.confirmed
    form.regras.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me

    return render_template('usuarios/edit_adm_perfil.html', form=form, user=user)


@bp.route('/register', methods=[ 'GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuario(
            email=form.email.data,
            user_name=form.user_name.data,
            password=form.password.data
        )

        database.session.add(user)
        database.session.commit()
        flash('Você pode fazer login!')
        return redirect(url_for('bp.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.senha.data):
            login_user(user, form.lembrar_de_mim.data)
            next = request.args.get('next')
        
            if next is None or not next.startswith('/'):
                next = url_for('bp.index') # nome da função view acossiada

            return redirect(next)

        flash('Username ou senha invalidos')

    return render_template('auth/login.html', form=form)


@bp.route('/unconfirmed')
def unconfirmed():
    pass


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado!')
    return redirect(url_for('bp.index'))


@bp.app_context_processor
def inject_permissions():
    """
    Processador de contexto deixa uma variavel disponível a todos
    os templates durante a renderização.
    """
    return dict(Permissions=Permissions)


@bp.before_app_request
def atualization_ping():

    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint and request.blueprint != 'bp' and request.endpoint != 'static':
            return redirect(url_for('bp.unconfirmed'))


def configure(app):
    app.register_blueprint(bp)