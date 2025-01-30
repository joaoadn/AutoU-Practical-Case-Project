from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch

# Caminhos para os arquivos de dados
data_dir = "../data"
produtivo_path = os.path.join(data_dir, "produtivo.txt")
improdutivo_path = os.path.join(data_dir, "improdutivo.txt")

# Função para carregar dados de um arquivo
def load_data(file_path, label):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    return lines, [label] * len(lines)

# Carregar dados produtivos e improdutivos
produtivo_texts, produtivo_labels = load_data(produtivo_path, 1)  # 1 para produtivo
improdutivo_texts, improdutivo_labels = load_data(improdutivo_path, 0)  # 0 para improdutivo

# Combinar dados
texts = produtivo_texts + improdutivo_texts
labels = produtivo_labels + improdutivo_labels

# Criar um dataset do Hugging Face
dataset = Dataset.from_dict({'text': texts, 'label': labels})

# Carregar o tokenizer
tokenizer = AutoTokenizer.from_pretrained("D:/Program Files (x86)/VsCode/UFLA/UFLA - 2024.2/Inteligencia-Artificial/AutoU-Practical-Case-Project/models/bert-portuguese")

# Função para tokenização
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

# Tokenizar o dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Carregar o modelo
model = AutoModelForSequenceClassification.from_pretrained(
    "D:/Program Files (x86)/VsCode/UFLA/UFLA - 2024.2/Inteligencia-Artificial/AutoU-Practical-Case-Project/models/bert-portuguese", 
    num_labels=2
)

# Função para calcular métricas
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

# Configurar o treinamento
training_args = TrainingArguments(
    output_dir="../models/email-classifier",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    evaluation_strategy="epoch",
)

# Criar o Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    compute_metrics=compute_metrics,
)

# Treinar o modelo
trainer.train()

# Salvar o modelo treinado
trainer.save_model("../models/email-classifier")
print("Modelo treinado salvo em ../models/email-classifier")