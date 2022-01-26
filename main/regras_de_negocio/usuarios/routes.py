from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from main.regras_de_negocio.governancia.models import Permissions
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
    return render_template('usuarios/perfil.html', user=user)


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


@bp.route('/admin')
@login_required
@admin_required
def apenas_adms():
    return {'message':'Apenas AMDs'}


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