import unittest
from app import app, preprocess_text, allowed_file

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_preprocess_text(self):
        text = "Este é um exemplo de texto para pré-processamento."
        processed_text = preprocess_text(text)
        self.assertIsInstance(processed_text, str)
        self.assertNotIn("é", processed_text)  # Verifica se as stopwords foram removidas
    
    def test_allowed_file(self):
        self.assertTrue(allowed_file("teste.txt"))
        self.assertTrue(allowed_file("documento.pdf"))
        self.assertFalse(allowed_file("imagem.png"))
    
    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_process_email_route(self):
        response = self.app.post('/process', json={'email': 'Olá, gostaria de agendar uma reunião.'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.json)
        self.assertIn('response', response.json)

if __name__ == '__main__':
    unittest.main()