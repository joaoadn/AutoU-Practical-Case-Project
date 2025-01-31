import pandas as pd
import joblib
import logging
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from config import MODEL_PATH, BASE_DIR

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Parâmetros globais para reprodutibilidade e otimização
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Função para avaliar o modelo
def evaluate_model(model, X_test, y_test):
    """
    Avalia o modelo usando métricas de classificação.
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        "Acurácia": accuracy_score(y_test, y_pred),
        "Precisão": precision_score(y_test, y_pred, average='weighted'),
        "Recall": recall_score(y_test, y_pred, average='weighted'),
        "F1-Score": f1_score(y_test, y_pred, average='weighted'),
    }

    for metric, value in metrics.items():
        logger.info(f"{metric}: {value:.4f}")

    return metrics

# Função principal
def train_model():
    try:
        # Carregar dados
        train_data_path = BASE_DIR / "data/email_training_data.csv"
        if not train_data_path.exists():
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {train_data_path}")

        train_data = pd.read_csv(train_data_path)
        logger.info(f"Total de registros carregados: {len(train_data)}")

        # Verificar balanceamento das classes
        class_distribution = train_data["label"].value_counts(normalize=True)
        logger.info(f"Distribuição das classes (%):\n{class_distribution * 100}")

        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            train_data["text"], train_data["label"], test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=train_data["label"]
        )
        logger.info(f"Tamanho do conjunto de treino: {len(X_train)}")
        logger.info(f"Tamanho do conjunto de teste: {len(X_test)}")

        # Otimizar TF-IDF removendo palavras muito comuns e raras
        vectorizer = TfidfVectorizer(
            stop_words="portuguese",
            max_df=0.95,  # Ignora termos que aparecem em mais de 95% dos emails
            min_df=2,  # Ignora termos que aparecem em menos de 2 emails
            ngram_range=(1, 2)  # Considera unigramas e bigramas
        )

        # Criar pipeline otimizado
        model = Pipeline([
            ("tfidf", vectorizer),
            ("clf", MultinomialNB(alpha=0.1))  # Suavização para lidar melhor com dados esparsos
        ])

        # Treinar modelo
        model.fit(X_train, y_train)
        logger.info("Modelo treinado com sucesso")

        # Avaliar modelo
        logger.info("Avaliando modelo no conjunto de teste...")
        evaluate_model(model, X_test, y_test)

        # Salvar modelo
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        logger.info(f"Modelo salvo em: {MODEL_PATH}")

    except Exception as e:
        logger.error(f"Erro ao treinar o modelo: {e}", exc_info=True)

if __name__ == "__main__":
    train_model()