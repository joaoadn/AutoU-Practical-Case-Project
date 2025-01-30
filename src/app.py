from flask import Flask, request, jsonify, send_from_directory
import joblib
import os
from openai import OpenAI
from werkzeug.utils import secure_filename
import PyPDF2
from config import (
    logger, rate_limit, validate_file_size, 
    cache_response, MAX_FILE_SIZE
)

app = Flask(__name__, static_url_path='/static', static_folder='../static')

# Carregar o modelo treinado
try:
    model_path = os.path.join(os.path.dirname(__file__), '../models/email-classifier/model.joblib')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")
    model = joblib.load(model_path)
    logger.info("Modelo carregado com sucesso")
except Exception as e:
    logger.error(f"Erro ao carregar modelo: {e}")
    raise

# Inicializar o cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {e}")
        raise

def classify_email(email_text):
    try:
        prediction = model.predict([email_text])
        return "produtivo" if prediction[0] == 1 else "improdutivo"
    except Exception as e:
        logger.error(f"Erro na classificação: {e}")
        raise

@app.route('/')
def serve_static():
    return "Bem-vindo ao Classificador de Emails!"

@app.route('/process', methods=['POST'])
@rate_limit
@cache_response()
def process_email():
    try:
        # Verificar se é upload de arquivo ou texto
        if 'file' in request.files:
            file = request.files['file']
            
            if not validate_file_size(file):
                return jsonify({'error': f'Arquivo muito grande. Máximo: {MAX_FILE_SIZE/1024/1024}MB'}), 400
                
            if file.filename.endswith('.pdf'):
                content = extract_text_from_pdf(file)
            elif file.filename.endswith('.txt'):
                content = file.read().decode('utf-8')
            else:
                return jsonify({'error': 'Formato de arquivo não suportado'}), 400
        else:
            data = request.json
            if not data or 'email' not in data:
                return jsonify({'error': 'Texto do email é obrigatório'}), 400
            content = data['email']

        # Log do processamento
        logger.info(f"Processando email: {content[:100]}...")

        # Classificação do email
        category = classify_email(content)
        
        # Geração de Resposta usando OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente profissional que gera respostas para emails."},
                {"role": "user", "content": content}
            ]
        )
        
        result = {
            'category': category,
            'response': response.choices[0].message.content
        }
        
        logger.info(f"Email processado com sucesso. Categoria: {category}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)