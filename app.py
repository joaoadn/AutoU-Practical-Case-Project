from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from transformers import pipeline
from dotenv import load_dotenv

import os

app = Flask(__name__)

load_dotenv()  # Carregar variáveis do arquivo .env

# Usando a variável de ambiente normalmente
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



# Inicializar o classificador com um modelo mais apropriado para classificação de texto
classifier = pipeline(
    "text-classification",
    model="facebook/bart-large-mnli",  # Modelo mais adequado para classificação de texto
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
            candidate_labels=["produtivo", "improdutivo", "urgente", "não urgente"]
        )
        
        # Pegar a categoria com maior score
        category = classification_result[0][0]['label']
        
        # Geração de Resposta usando a nova API do OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente profissional que gera respostas para emails."},
                {"role": "user", "content": f"Gere uma resposta profissional para o seguinte email: {email_text}"}
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