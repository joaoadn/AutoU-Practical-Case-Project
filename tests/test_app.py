import unittest
from src.app import app

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
        self.assertIn('category', response.json)
        self.assertIn('response', response.json)
        self.assertEqual(response.json['category'], 'produtivo')

    def test_email_classification_unproductive(self):
        # Teste com um email que deve ser improdutivo
        email_improdutivo = {
            'email': 'Obrigado pela ajuda com o sistema ontem!'
        }
        
        response = self.app.post('/process', json=email_improdutivo)
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.json)
        self.assertIn('response', response.json)
        self.assertEqual(response.json['category'], 'improdutivo')

    def test_invalid_email_input(self):
        # Teste com uma entrada inválida
        invalid_email = {
            'email': ''
        }
        
        response = self.app.post('/process', json=invalid_email)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_missing_email_field(self):
        # Teste com um campo de email ausente
        missing_email_field = {}
        
        response = self.app.post('/process', json=missing_email_field)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()