from flask import Blueprint, session, render_template, redirect, url_for

from main.regras_de_negocio.usuarios.models import Usuario
from main.formularios.models import Usuario as UserTamplete
from main import database

bp = Blueprint('bp', __name__, url_prefix='/user')

@bp.route('/', methods=['GET', 'POST'])
def user():
    
    form = UserTamplete()
    if form.validate_on_submit():

        user = Usuario.query.filter_by(user_name=form.name.data).first()
        if user is None:

            user = Usuario(user_name=form.name.data)
            database.session.add(user)
            database.session.commit()

            session['know'] = False

        else:
            session['know'] = True

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('bp.user'))

    return render_template(
        'pagina_inicial/user.html',
        form=form,
        name=session.get('name'),
        know=session.get('know', False)
    )

def configure(app):
    app.register_blueprint(bp)