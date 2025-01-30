import unittest
from src.app import app, preprocess_text, allowed_file

class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_email_classification_productive(self):
        # Teste com um email que deve ser produtivo
        email_produtivo = {
            'email': 'Preciso de suporte técnico urgente. O sistema está fora do ar desde às 14h.'
        }
        
        response = self.app.post('/process', json=email_produtivo)
        self.assertEqual(response.status_code, 200)
        # Adicione mais verificações conforme necessário, por exemplo:
        # self.assertIn('produtivo', response.json['classification'])

    def test_email_classification_unproductive(self):
        # Teste com um email que deve ser improdutivo
        email_improdutivo = {
            'email': 'Obrigado pela ajuda com o sistema ontem!'
        }
        
        response = self.app.post('/process', json=email_improdutivo)
        self.assertEqual(response.status_code, 200)
        # Adicione mais verificações conforme necessário, por exemplo:
        # self.assertIn('improdutivo', response.json['classification'])

if __name__ == '__main__':
    unittest.main()