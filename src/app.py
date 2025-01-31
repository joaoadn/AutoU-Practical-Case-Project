from flask import Flask, request, jsonify
import joblib
from openai import OpenAI
from config import FLASK_CONFIG, MODEL_PATH, OPENAI_API_KEY
import PyPDF2
import logging
import os
from functools import lru_cache

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar o Flask
app = Flask(__name__)
app.config.update(FLASK_CONFIG)

# Carregar o modelo (com cache para evitar recarregamento)
@lru_cache(maxsize=1)
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        logger.info("Modelo carregado com sucesso")
        return model
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        raise

model = load_model()

# Inicializar o cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Função para extrair texto de PDF
def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() for page in pdf_reader.pages)
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente profissional que gera respostas para emails."},
                {"role": "user", "content": content}
            ],
            max_tokens=100  # Limita o tamanho da resposta
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        return "Desculpe, não foi possível gerar uma resposta."

# Rota para processar emails
@app.route('/process', methods=['POST'])
def process_email():
    try:
        # Verifica se o arquivo foi enviado
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.pdf'):
                content = extract_text_from_pdf(file)
            else:
                content = file.read().decode('utf-8')
        else:
            data = request.json
            content = data.get('email', '')

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

# Inicialização do servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)