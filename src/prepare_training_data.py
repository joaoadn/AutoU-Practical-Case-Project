import pandas as pd
import os
import re
import logging
from pathlib import Path

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Caminho para salvar o arquivo CSV
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_PATH = DATA_DIR / "email_training_data.csv"

# Verifica se a pasta de dados existe, caso contrário, cria
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Compilação de regex para melhor performance
RE_NUMBERS = re.compile(r'\d+')
RE_SPACES = re.compile(r'\s+')
RE_PUNCTUATION = re.compile(r'[^\w\s]')

def clean_text(text: str) -> str:
    """
    Limpa e normaliza o texto:
    - Converte para minúsculas
    - Remove números
    - Remove espaços extras
    - Remove pontuação
    """
    text = text.lower()
    text = RE_NUMBERS.sub('', text)  # Remove números
    text = RE_SPACES.sub(' ', text)  # Remove espaços extras
    text = RE_PUNCTUATION.sub('', text)  # Remove pontuação
    return text.strip()

def get_training_data() -> pd.DataFrame:
    """
    Retorna um DataFrame com exemplos de emails e suas labels.
    """
    data = [
        # Emails Produtivos
        ("Preciso de suporte técnico urgente. O sistema está fora do ar desde às 14h.", 1),
        ("Por favor, pode me ajudar com o erro #1234 que está aparecendo no módulo de relatórios?", 1),
        ("Solicito atualização sobre o caso #5678 aberto na semana passada.", 1),
        ("Preciso agendar uma reunião para discutir o projeto XYZ.", 1),
        ("O relatório mensal de vendas está pronto para revisão.", 1),
        # Emails Improdutivos
        ("Olá, como você está? Vamos marcar um café?", 0),
        ("Você viu o último episódio daquela série? Está incrível!", 0),
        ("Feliz aniversário! Espero que tenha um dia maravilhoso.", 0),
        ("Ei, vamos jogar futebol no final de semana?", 0),
        ("Você já experimentou o novo restaurante da esquina?", 0),
    ]
    df = pd.DataFrame(data, columns=["text", "label"])
    df["text"] = df["text"].apply(clean_text)
    return df

def append_to_dataset(new_data: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    """
    Adiciona novos dados ao dataset existente (se o arquivo já existir).
    """
    if output_path.exists():
        existing_data = pd.read_csv(output_path)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True).drop_duplicates()
    else:
        updated_data = new_data
    return updated_data

def prepare_training_data():
    try:
        # Obter dados de exemplo e normalizar
        df = get_training_data()

        # Adicionar ao dataset existente (evitando duplicatas)
        df = append_to_dataset(df, OUTPUT_PATH)

        # Salvar como CSV
        df.to_csv(OUTPUT_PATH, index=False)
        logger.info(f"Dados de treinamento salvos em: {OUTPUT_PATH}")
        logger.info(f"Total de registros: {len(df)}")
        logger.info(f"Distribuição das labels:\n{df['label'].value_counts()}")

    except Exception as e:
        logger.error(f"Erro ao preparar dados de treinamento: {e}", exc_info=True)

if __name__ == '__main__':
    prepare_training_data()