from flask import Flask, request, jsonify
import joblib
import openai
import logging
import os
from functools import lru_cache
from pdfplumber import open as pdf_open  # Alternativa mais leve e eficiente a PyPDF2

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar o Flask
app = Flask(__name__)
app.config.from_object('config.FLASK_CONFIG')  # Configuração direto do arquivo

# Carregar o modelo (com cache para evitar recarregamento)
@lru_cache(maxsize=1)
def load_model():
    try:
        model = joblib.load(os.getenv('MODEL_PATH', 'model.pkl'))  # Melhor usar variável de ambiente para caminho
        logger.info("Modelo carregado com sucesso")
        return model
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        raise

model = load_model()

# Função para extrair texto de PDF
def extract_text_from_pdf(file):
    try:
        with pdf_open(file) as pdf:
            return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {e}")
        return ""

# Função para classificar o email
def classify_email(content):
    try:
        return model.predict([content])[0]
    except Exception as e:
        logger.error(f"Erro ao classificar email: {e}")
        return "improdutivo"

# Função para gerar resposta automática
def generate_response(content):
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')  # Definir a chave API de forma segura
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente profissional que gera respostas para emails."},
                {"role": "user", "content": content}
            ],
            max_tokens=100
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        return "Desculpe, não foi possível gerar uma resposta."

# Rota para processar emails
@app.route('/process', methods=['POST'])
def process_email():
    try:
        # Verifica se o arquivo foi enviado
        file = request.files.get('file')
        if file:
            content = extract_text_from_pdf(file) if file.filename.endswith('.pdf') else file.read().decode('utf-8')
        else:
            content = request.json.get('email', '')

        # Validação do conteúdo
        if not content.strip():
            return jsonify({'error': 'Texto do email é obrigatório'}), 400

        # Classificação e geração de resposta
        category = classify_email(content)
        response_content = generate_response(content)

        return jsonify({'category': category, 'response': response_content}), 200

    except Exception as e:
        logger.error(f"Erro ao processar o email: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao processar o email'}), 500

# Handler para o Vercel
def vercel_handler(request):
    from flask import Response

    # Converte a requisição do Vercel para o formato do Flask
    with app.request_context(request):
        try:
            response = app.full_dispatch_request()
        except Exception as e:
            logger.error(f"Erro ao processar requisição: {e}", exc_info=True)
            response = app.make_response(jsonify({'error': 'Erro interno no servidor'}), 500)
        return Response(response.get_data(), status=response.status_code, headers=dict(response.headers))

# Inicialização do servidor (para rodar localmente)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)