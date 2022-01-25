import unittest
from main.regras_de_negocio.usuarios.models import Usuario

class UserModelTestCase(unittest.TestCase):

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