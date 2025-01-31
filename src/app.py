from flask import Flask, request, jsonify
import joblib
import openai
import logging
import os
from functools import lru_cache
import pdfplumber  # Correção da importação

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar o Flask
app = Flask(__name__)

# Carregar o modelo (com cache para evitar recarregamento)
@lru_cache(maxsize=1)
def load_model():
    try:
        model_path = os.getenv('MODEL_PATH', 'model.pkl')  # Melhor usar variável de ambiente para caminho
        model = joblib.load(model_path)
        logger.info("Modelo carregado com sucesso")
        return model
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        raise

model = load_model()

# Função para extrair texto de PDF
def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
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

# Inicialização do servidor (para rodar no Render)
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Render define a porta automaticamente
    app.run(host='0.0.0.0', port=port)