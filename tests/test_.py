import sys
import os
import unittest
from io import BytesIO
import logging

# Adicionar o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.app import app

class TestApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Configura o ambiente de teste, que é executado uma única vez antes de todos os testes.
        """
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.INFO)

        # Configurar logs para exibir no console durante os testes
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not cls.logger.handlers:  # Evita adicionar múltiplos handlers
            cls.logger.addHandler(handler)

    def setUp(self):
        """
        Configura o ambiente de cada teste.
        """
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        """
        Limpa o ambiente de teste.
        """
        pass

    def _post_email(self, email_data):
        """
        Função auxiliar para evitar repetição de código ao testar diferentes tipos de email.
        """
        return self.app.post('/process', json=email_data)

    def test_email_classification_productive(self):
        """
        Testa a classificação de um email produtivo.
        """
        email_produtivo = {
            'email': 'Preciso de suporte técnico urgente. O sistema está fora do ar desde às 14h.'
        }
        
        response = self._post_email(email_produtivo)
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.json)
        self.assertIn('response', response.json)
        self.assertEqual(response.json['category'], 'produtivo')
        self.logger.info("Teste de email produtivo concluído com sucesso.")

    def test_email_classification_unproductive(self):
        """
        Testa a classificação de um email improdutivo.
        """
        email_improdutivo = {
            'email': 'Obrigado pela ajuda com o sistema ontem!'
        }
        
        response = self._post_email(email_improdutivo)
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.json)
        self.assertIn('response', response.json)
        self.assertEqual(response.json['category'], 'improdutivo')
        self.logger.info("Teste de email improdutivo concluído com sucesso.")

    def test_invalid_email_input(self):
        """
        Testa a resposta da API para uma entrada inválida (email vazio).
        """
        invalid_email = {
            'email': ''
        }
        
        response = self._post_email(invalid_email)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.logger.info("Teste de entrada inválida concluído com sucesso.")

    def test_missing_email_field(self):
        """
        Testa a resposta da API para um campo de email ausente.
        """
        missing_email_field = {}
        
        response = self._post_email(missing_email_field)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.logger.info("Teste de campo de email ausente concluído com sucesso.")

    def test_pdf_file_processing(self):
        """
        Testa o processamento de um arquivo PDF.
        """
        pdf_content = b"%PDF-1.4\n1 0 obj\n<</Type /Catalog /Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type /Pages /Kids [3 0 R] /Count 1>>\nendobj\n3 0 obj\n<</Type /Page /Parent 2 0 R /Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 44>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000110 00000 n\n0000000190 00000 n\ntrailer\n<</Size 5 /Root 1 0 R>>\nstartxref\n268\n%%EOF"
        pdf_file = BytesIO(pdf_content)
        pdf_file.filename = "test.pdf"

        response = self.app.post('/process', data={'file': (pdf_file, pdf_file.filename)})
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.json)
        self.assertIn('response', response.json)
        self.logger.info("Teste de processamento de PDF concluído com sucesso.")

    def test_openai_response_format(self):
        """
        Testa se a resposta da OpenAI está no formato esperado.
        """
        email_produtivo = {
            'email': 'Preciso de suporte técnico urgente. O sistema está fora do ar desde às 14h.'
        }
        
        response = self._post_email(email_produtivo)
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json)
        self.assertIsInstance(response.json['response'], str)
        self.logger.info("Teste de formato da resposta da OpenAI concluído com sucesso.")

    def test_model_error_handling(self):
        """
        Testa o tratamento de erros no carregamento do modelo.
        """
        original_model_path = app.config['MODEL_PATH']
        app.config['MODEL_PATH'] = "invalid/path/model.joblib"

        email_produtivo = {
            'email': 'Preciso de suporte técnico urgente. O sistema está fora do ar desde às 14h.'
        }
        
        response = self._post_email(email_produtivo)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)

        # Restaurar o caminho original do modelo
        app.config['MODEL_PATH'] = original_model_path
        self.logger.info("Teste de tratamento de erro no modelo concluído com sucesso.")

if __name__ == '__main__':
    unittest.main()