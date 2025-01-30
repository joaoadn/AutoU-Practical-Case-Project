import pandas as pd
import os
import re
import logging
from pathlib import Path

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho para salvar o arquivo CSV
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(BASE_DIR, "data")
output_path = os.path.join(DATA_DIR, "email_training_data.csv")

# Verifica se a pasta de dados existe, caso contrário, cria
os.makedirs(DATA_DIR, exist_ok=True)

# Função para limpar e normalizar o texto
def clean_text(text):
    """
    Limpa e normaliza o texto:
    - Converte para minúsculas
    - Remove números
    - Remove espaços extras
    - Remove pontuação
    """
    text = text.lower()  # Converte para minúsculas
    text = re.sub(r'\d+', '', text)  # Remove números
    text = re.sub(r'\s+', ' ', text)  # Remove espaços extras
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    return text.strip()

# Dados de exemplo para treinamento
def get_training_data():
    """
    Retorna um dicionário com exemplos de emails e suas labels.
    """
    return {
        'text': [
            # Emails Produtivos
            "Preciso de suporte técnico urgente. O sistema está fora do ar desde às 14h.",
            "Por favor, pode me ajudar com o erro #1234 que está aparecendo no módulo de relatórios?",
            "Solicito atualização sobre o caso #5678 aberto na semana passada.",
            "Preciso agendar uma reunião para discutir o projeto XYZ.",
            "O relatório mensal de vendas está pronto para revisão.",
            # Emails Improdutivos
            "Olá, como você está? Vamos marcar um café?",
            "Você viu o último episódio daquela série? Está incrível!",
            "Feliz aniversário! Espero que tenha um dia maravilhoso.",
            "Ei, vamos jogar futebol no final de semana?",
            "Você já experimentou o novo restaurante da esquina?",
        ],
        'label': [
            # Labels correspondentes (1 para produtivo, 0 para improdutivo)
            1,  # Produtivo
            1,  # Produtivo
            1,  # Produtivo
            1,  # Produtivo
            1,  # Produtivo
            0,  # Improdutivo
            0,  # Improdutivo
            0,  # Improdutivo
            0,  # Improdutivo
            0,  # Improdutivo
        ]
    }

# Função para adicionar novos dados ao dataset existente
def append_to_dataset(new_data, output_path):
    """
    Adiciona novos dados ao dataset existente (se o arquivo já existir).
    """
    if os.path.exists(output_path):
        existing_data = pd.read_csv(output_path)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data
    return updated_data

# Função principal
def prepare_training_data():
    try:
        # Obter dados de exemplo
        training_data = get_training_data()

        # Limpar e normalizar os textos
        training_data['text'] = [clean_text(text) for text in training_data['text']]

        # Criar um DataFrame
        df = pd.DataFrame(training_data)

        # Adicionar ao dataset existente (se houver)
        df = append_to_dataset(df, output_path)

        # Salvar como CSV
        df.to_csv(output_path, index=False)
        logger.info(f"Dados de treinamento salvos em: {output_path}")
        logger.info(f"Total de registros: {len(df)}")
        logger.info(f"Distribuição das labels:\n{df['label'].value_counts()}")

    except Exception as e:
        logger.error(f"Erro ao preparar dados de treinamento: {e}")

if __name__ == '__main__':
    prepare_training_data()