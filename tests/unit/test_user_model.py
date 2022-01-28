import unittest
from main import create_app, database
from main.regras_de_negocio.governancia.models import Permissions, RegrasDeAcesso
from main.regras_de_negocio.usuarios.dominio.orm.models import Usuario

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        database.create_all()
        RegrasDeAcesso.inserir_regras()
    
    
    def tearDown(self):
        database.session.remove()
        database.drop_all()
        self.app_context.pop()


    def test_atribuir_senha(self):
        user = Usuario(password='gato')
        self.assertTrue(user.password_hash is not None)
    

    def test_pegar_retorna_execao(self):
        user = Usuario(password='gato')
        with self.assertRaises(AttributeError):
            user.password


    def test_verificacao_de_senhas(self):
        user = Usuario(password='gato')
        self.assertTrue(user.verify_password('gato'))
        self.assertFalse(user.verify_password('cachorro'))

    
    def test_hash_das_senhas_sao_aleatorios(self):
        user_1 = Usuario(password='gato')
        user_2 = Usuario(password='gato')

        self.assertTrue(user_1.password_hash != user_2.password_hash)
    
    
    def test_regras_de_acesso_do_usuario(self):
        user = Usuario(email='othon@teste.com' ,password='gato')
        self.assertTrue(user.can(Permissions.ADICIONAR_AO_CARRINHO))