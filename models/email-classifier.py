import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
import logging
from pathlib import Path

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho para o arquivo CSV de treinamento
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = os.path.join(BASE_DIR, "data/email_training_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models/email-classifier")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

def load_data(csv_path):
    """
    Carrega os dados de treinamento a partir de um arquivo CSV.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")

    data = pd.read_csv(csv_path)
    if "text" not in data.columns or "label" not in data.columns:
        raise ValueError("O arquivo CSV deve conter as colunas 'text' e 'label'.")

    return data

def evaluate_model(model, X_test, y_test):
    """
    Avalia o modelo usando métricas de classificação.
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average='weighted')
    recall = recall_score(y_test, predictions, average='weighted')
    f1 = f1_score(y_test, predictions, average='weighted')

    logger.info(f"Acurácia: {accuracy:.2f}")
    logger.info(f"Precisão: {precision:.2f}")
    logger.info(f"Recall: {recall:.2f}")
    logger.info(f"F1-Score: {f1:.2f}")

    # Exibir relatório de classificação
    logger.info("Relatório de Classificação:\n" + classification_report(y_test, predictions))

def train_model():
    try:
        # Carregar dados
        data = load_data(CSV_PATH)
        logger.info(f"Total de registros carregados: {len(data)}")

        # Verificar balanceamento das classes
        class_distribution = data['label'].value_counts()
        logger.info(f"Distribuição das classes:\n{class_distribution}")

        # Dividir os dados em treino e teste
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            data["text"], data["label"], test_size=0.2, random_state=42
        )
        logger.info(f"Tamanho do conjunto de treino: {len(train_texts)}")
        logger.info(f"Tamanho do conjunto de teste: {len(val_texts)}")

        # Criar um pipeline de TF-IDF e Naive Bayes
        model = make_pipeline(TfidfVectorizer(), MultinomialNB())

        # Treinar o modelo
        logger.info("Treinando o modelo...")
        model.fit(train_texts, train_labels)

        # Avaliar o modelo no conjunto de teste
        logger.info("Avaliando o modelo no conjunto de teste...")
        evaluate_model(model, val_texts, val_labels)

        # Validação cruzada
        logger.info("Realizando validação cruzada...")
        cv_scores = cross_val_score(model, data["text"], data["label"], cv=5, scoring='accuracy')
        logger.info(f"Acurácia média na validação cruzada: {cv_scores.mean():.2f}")

        # Salvar o modelo treinado
        os.makedirs(MODEL_DIR, exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        logger.info(f"Modelo salvo em: {MODEL_PATH}")

    except Exception as e:
        logger.error(f"Erro ao treinar o modelo: {e}")

if __name__ == '__main__':
    train_model()