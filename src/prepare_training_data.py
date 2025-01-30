import pandas as pd
import os
import re

# Caminho para salvar o arquivo CSV
output_path = os.path.join(os.path.dirname(__file__), '../data/email_training_data.csv')

# Verifica se a pasta de dados existe, caso contrário, cria
if not os.path.exists(os.path.dirname(output_path)):
    os.makedirs(os.path.dirname(output_path))

# Função para limpar e normalizar o texto
def clean_text(text):
    text = text.lower()  # Converte para minúsculas
    text = re.sub(r'\d+', '', text)  # Remove números
    text = re.sub(r'\s+', ' ', text)  # Remove espaços extras
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    return text

# Dados de exemplo para treinamento
training_data = {
    'text': [
        # Emails Produtivos
        "Preciso de suporte técnico urgente. O sistema está fora do ar desde às 14h.",
        "Por favor, pode me ajudar com o erro #1234 que está aparecendo no módulo de relatórios?",
        "Solicito atualização sobre o caso #5678 aberto na semana passada.",
        # Adicione mais exemplos conforme necessário
    ],
    'label': [
        # Labels correspondentes (1 para produtivo, 0 para improdutivo)
        1,
        1,
        1,
        # Adicione mais labels conforme necessário
    ]
}

# Limpar e normalizar os textos
training_data['text'] = [clean_text(text) for text in training_data['text']]

# Criar um DataFrame e salvar como CSV
df = pd.DataFrame(training_data)
df.to_csv(output_path, index=False)
print(f"Dados de treinamento salvos em: {output_path}")