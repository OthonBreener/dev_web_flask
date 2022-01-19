from os import getenv
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from formularios.models import Usuario


app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')


bootsprap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def user():
    form = Usuario()
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
