from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootsprap = Bootstrap(app)

@app.route('/')
def user():
    return render_template('pagina_inicial/user.html')


#rotas de erro
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500
