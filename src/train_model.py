from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch

# Carregar o dataset
dataset = load_dataset('csv', data_files='../data/email_training_data.csv')

# Carregar o tokenizer
tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")

# Função para tokenização
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

# Tokenizar o dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Carregar o modelo
model = AutoModelForSequenceClassification.from_pretrained(
    "neuralmind/bert-base-portuguese-cased", 
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
    train_dataset=tokenized_datasets["train"],
    compute_metrics=compute_metrics,
)

# Treinar o modelo
trainer.train()

# Salvar o modelo treinado
trainer.save_model("../models/email-classifier")
print("Modelo treinado salvo em ../models/email-classifier")