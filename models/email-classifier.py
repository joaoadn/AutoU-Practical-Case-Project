from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
import pandas as pd
import os
import joblib

# Verificar se o arquivo CSV existe
csv_path = "../data/email_training_data.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")

# Carregar dados de treinamento
data = pd.read_csv(csv_path)

# Verificar se as colunas "text" e "label" existem no CSV
if "text" not in data.columns or "label" not in data.columns:
    raise ValueError("O arquivo CSV deve conter as colunas 'text' e 'label'.")

# Pré-processar os dados
texts = data["text"].tolist()
labels = data["label"].tolist()

# Dividir os dados em treino e teste
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Criar um pipeline de TF-IDF e Naive Bayes
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Treinar o modelo
model.fit(train_texts, train_labels)

# Avaliar o modelo
predictions = model.predict(val_texts)
print(classification_report(val_labels, predictions))

# Salvar o modelo treinado
output_model_dir = "../models/email-classifier"
if not os.path.exists(output_model_dir):
    os.makedirs(output_model_dir)
joblib.dump(model, os.path.join(output_model_dir, "model.joblib"))
print(f"Modelo treinado e salvo em: {output_model_dir}")