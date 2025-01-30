from flask import Flask, request, jsonify
import joblib
import os
from openai import OpenAI

app = Flask(__name__)

# Carregar o modelo treinado
model_path = "../models/email-classifier/model.joblib"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Modelo não encontrado: {model_path}")
model = joblib.load(model_path)

# Inicializar o cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função para classificar o email
def classify_email(email_text):
    prediction = model.predict([email_text])
    return "produtivo" if prediction[0] == 1 else "improdutivo"

# Rota para processar o email
@app.route('/process', methods=['POST'])
def process_email():
    try:
        data = request.json
        if not data or 'email' not in data:
            return jsonify({'error': 'Email text is required'}), 400
        email_text = data['email']
        
        # Classificação do email
        category = classify_email(email_text)
        
        # Geração de Resposta usando a nova API do OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente profissional que gera respostas para emails."},
                {"role": "user", "content": email_text}
            ]
        )
        
        return jsonify({
            'category': category,
            'response': response['choices'][0]['message']['content']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)