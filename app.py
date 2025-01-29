from flask import Flask, request, jsonify, render_template
import openai
from transformers import pipeline

app = Flask(__name__)

# Configurações
openai.api_key = "sua_chave_api"  # Substitua pela sua chave da OpenAI
classifier = pipeline("text-classification", model="distilbert-base-uncased")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_email():
    data = request.json
    email_text = data['email']

    # Classificação
    classification_result = classifier(email_text)
    category = "Produtivo" if classification_result[0]['label'] == "LABEL_1" else "Improdutivo"

    # Geração de Resposta
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Responda ao seguinte email de forma profissional: {email_text}",
        max_tokens=100
    )
    suggested_response = response.choices[0].text.strip()

    return jsonify({
        'category': category,
        'response': suggested_response
    })

if __name__ == '__main__':
    app.run(debug=True)