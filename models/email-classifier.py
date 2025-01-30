from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import pandas as pd
import torch
import os

# Verificar se o arquivo CSV existe
csv_path = "../data/email_training_data.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")

# Caminho para o modelo BERT em português
model_dir = "../models/bert-portuguese"

# Verificar se o diretório do modelo existe
if not os.path.exists(model_dir):
    raise FileNotFoundError(f"Diretório do modelo BERT não encontrado: {model_dir}")

# Carregar o modelo e o tokenizador
model = AutoModelForSequenceClassification.from_pretrained(model_dir, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# Carregar dados de treinamento
data = pd.read_csv(csv_path)

# Verificar se as colunas "text" e "label" existem no CSV
if "text" not in data.columns or "label" not in data.columns:
    raise ValueError("O arquivo CSV deve conter as colunas 'text' e 'label'.")

# Pré-processar os dados
texts = data["text"].tolist()
labels = data["label"].tolist()

# Tokenizar os textos
encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)

# Converter para formato de dataset do PyTorch
class EmailDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Dividir os dados em treino e teste
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2)
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

train_dataset = EmailDataset(train_encodings, train_labels)
val_dataset = EmailDataset(val_encodings, val_labels)

# Configurações de treinamento
training_args = TrainingArguments(
    output_dir="../models/email-classifier",  # Pasta para salvar o modelo treinado
    num_train_epochs=3,  # Número de épocas
    per_device_train_batch_size=8,  # Tamanho do batch
    per_device_eval_batch_size=8,
    logging_dir="../logs",  # Pasta para logs
    evaluation_strategy="epoch",  # Avaliar a cada época
    save_strategy="epoch",  # Salvar a cada época
    save_total_limit=2,  # Manter apenas os 2 últimos checkpoints
    load_best_model_at_end=True,  # Carregar o melhor modelo ao final
)

# Verificar se o diretório de logs existe, caso contrário, criar
if not os.path.exists("../logs"):
    os.makedirs("../logs")

# Inicializar o Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Treinar o modelo
trainer.train()

# Salvar o modelo treinado
trainer.save_model("../models/email-classifier")
tokenizer.save_pretrained("../models/email-classifier")
print("Modelo treinado e salvo em: ../models/email-classifier")