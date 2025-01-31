import os
import logging
import torch
import joblib
import numpy as np
from pathlib import Path
from datasets import load_dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from config import BASE_DIR, MODEL_PATH
from downloadmodel import model_name  # Importa o modelo baixado

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Definição de hiperparâmetros
BATCH_SIZE = 8
EPOCHS = 3
LEARNING_RATE = 2e-5

# Caminho do dataset
CSV_PATH = BASE_DIR / "data/email_training_data.csv"

# Caminho do diretório para salvar o modelo treinado
MODEL_DIR = BASE_DIR / "models/email-classifier"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Carregar o tokenizer uma única vez
tokenizer = AutoTokenizer.from_pretrained(model_name)

def load_data():
    """
    Carrega e converte os dados de treinamento para um formato compatível com transformers.
    """
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {CSV_PATH}")

    dataset = load_dataset("csv", data_files=str(CSV_PATH))["train"]
    dataset = dataset.train_test_split(test_size=0.2, stratify_by_column="label")  # Stratify mantém proporções
    return dataset

def tokenize_function(examples):
    """
    Tokeniza os textos usando o tokenizer do modelo do Hugging Face.
    """
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

def compute_metrics(eval_pred):
    """
    Calcula as métricas de avaliação do modelo.
    """
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    
    acc = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="weighted")
    
    return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}

def train_model():
    try:
        # Carregar dados
        dataset = load_data()
        dataset = dataset.map(tokenize_function, batched=True)

        # Configurar modelo
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

        # Configuração do treinamento
        training_args = TrainingArguments(
            output_dir=str(MODEL_DIR),
            evaluation_strategy="epoch",
            save_strategy="epoch",
            learning_rate=LEARNING_RATE,
            per_device_train_batch_size=BATCH_SIZE,
            per_device_eval_batch_size=BATCH_SIZE,
            num_train_epochs=EPOCHS,
            weight_decay=0.01,
            save_total_limit=1,  # Mantém apenas o último modelo salvo
            push_to_hub=False,
            logging_dir=str(MODEL_DIR / "logs"),
            logging_steps=10
        )

        # Criar trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset["train"],
            eval_dataset=dataset["test"],
            tokenizer=tokenizer,
            compute_metrics=compute_metrics
        )

        # Treinar o modelo
        logger.info("Treinando o modelo...")
        trainer.train()

        # Avaliação final
        logger.info("Avaliando modelo no conjunto de teste...")
        metrics = trainer.evaluate()
        logger.info(f"Métricas de avaliação: {metrics}")

        # Salvar modelo e tokenizer
        model.save_pretrained(str(MODEL_DIR))
        tokenizer.save_pretrained(str(MODEL_DIR))
        logger.info(f"Modelo salvo em: {MODEL_DIR}")

    except Exception as e:
        logger.error(f"Erro ao treinar o modelo: {e}", exc_info=True)

if __name__ == "__main__":
    train_model()