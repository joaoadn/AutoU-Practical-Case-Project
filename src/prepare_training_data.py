import pandas as pd
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

# Baixar recursos do NLTK (se necessário)
nltk.download('punkt')
nltk.download('stopwords')

# Função para pré-processamento de texto
def preprocess_text(text):
    # Tokenização
    tokens = word_tokenize(text.lower())
    # Remoção de stopwords
    stop_words = set(stopwords.words('portuguese'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    return " ".join(stemmed_tokens)

# Caminhos para os arquivos de dados
data_dir = "../data"  # Pasta onde os arquivos de dados estão
produtivo_path = os.path.join(data_dir, "produtivo.txt")  # Emails produtivos
improdutivo_path = os.path.join(data_dir, "produtivo.txt")  # Emails improdutivos

# Verificar se os arquivos de dados existem
if not os.path.exists(produtivo_path) or not os.path.exists(improdutivo_path):
    raise FileNotFoundError("Arquivos de dados não encontrados. Verifique os caminhos.")

# Função para carregar dados de um arquivo
def load_data(file_path, label):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    # Remove espaços em branco e linhas vazias
    lines = [line.strip() for line in lines if line.strip()]
    # Aplica pré-processamento
    processed_lines = [preprocess_text(line) for line in lines]
    return processed_lines, [label] * len(lines)

# Carregar dados produtivos e improdutivos
produtivo_texts, produtivo_labels = load_data(produtivo_path, 1)  # 1 para produtivo
improdutivo_texts, improdutivo_labels = load_data(improdutivo_path, 0)  # 0 para improdutivo

# Combinar dados
texts = produtivo_texts + improdutivo_texts
labels = produtivo_labels + improdutivo_labels

# Criar DataFrame
df = pd.DataFrame({'text': texts, 'label': labels})

# Salvar como CSV
output_path = os.path.join(data_dir, "email_training_data.csv")
df.to_csv(output_path, index=False)
print(f"Dados de treinamento salvos em {output_path}")