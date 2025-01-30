import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
import logging
from pathlib import Path
from config import MODEL_PATH, BASE_DIR

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para avaliar o modelo
def evaluate_model(model, X_test, y_test):
    """
    Avalia o modelo usando métricas de classificação.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    logger.info(f"Acurácia: {accuracy:.2f}")
    logger.info(f"Precisão: {precision:.2f}")
    logger.info(f"Recall: {recall:.2f}")
    logger.info(f"F1-Score: {f1:.2f}")

# Função principal
def train_model():
    try:
        # Carregar dados
        train_data_path = os.path.join(BASE_DIR, "data/email_training_data.csv")
        if not os.path.exists(train_data_path):
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {train_data_path}")

        train_data = pd.read_csv(train_data_path)
        logger.info(f"Total de registros carregados: {len(train_data)}")

        # Verificar balanceamento das classes
        class_distribution = train_data['label'].value_counts()
        logger.info(f"Distribuição das classes:\n{class_distribution}")

        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            train_data['text'], train_data['label'], test_size=0.2, random_state=42
        )
        logger.info(f"Tamanho do conjunto de treino: {len(X_train)}")
        logger.info(f"Tamanho do conjunto de teste: {len(X_test)}")

        # Treinar modelo
        model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB())
        ])
        model.fit(X_train, y_train)
        logger.info("Modelo treinado com sucesso")

        # Avaliar modelo
        logger.info("Avaliando modelo no conjunto de teste...")
        evaluate_model(model, X_test, y_test)

        # Salvar modelo
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        logger.info(f"Modelo salvo em: {MODEL_PATH}")

    except Exception as e:
        logger.error(f"Erro ao treinar o modelo: {e}")

if __name__ == '__main__':
    train_model()