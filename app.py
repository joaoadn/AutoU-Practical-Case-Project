from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from transformers import pipeline
from dotenv import load_dotenv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from werkzeug.utils import secure_filename
import PyPDF2

import os

nltk.download('punkt')
nltk.download('stopwords')


app = Flask(__name__)

load_dotenv()  # Carregar variáveis do arquivo .env

# Usando a variável de ambiente normalmente
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Pré processamento de texto
def preprocess_text(text):
    # Tokenização
    tokens = word_tokenize(text.lower())
    # Remoção de stop words
    stop_words = set(stopwords.words('portuguese'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    return " ".join(stemmed_tokens)

email_text = preprocess_text(data['email'])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    if filename.endswith('.txt'):
        email_text = file.read().decode('utf-8')
    elif filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        email_text = ""
        for page in reader.pages:
            email_text += page.extract_text()
    else:
        return jsonify({'error': 'Unsupported file format'}), 400
    
    # Processar o email_text como antes
    return process_email(email_text)

# Inicializar o classificador com um modelo mais apropriado para classificação de texto
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased",  # Modelo mais leve
    return_all_scores=True
)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_email():
    try:
        data = request.json
        if not data or 'email' not in data:
            return jsonify({'error': 'Email text is required'}), 400
        
        email_text = data['email']
        
        # Classificação com categorias específicas
        classification_result = classifier(
        email_text,
        candidate_labels=["produtivo", "improdutivo"]
)
        
        # Pegar a categoria com maior score
        category = classification_result[0][0]['label']
        
        # Geração de Resposta usando a nova API do OpenAI
        response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um assistente profissional que gera respostas para emails."},
        {"role": "user", "content": f"O email foi classificado como '{category}'. Gere uma resposta profissional para o seguinte email: {email_text}"}
    ],
    max_tokens=150
)
        
        suggested_response = response.choices[0].message.content.strip()
        
        return jsonify({
            'category': category,
            'response': suggested_response
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    