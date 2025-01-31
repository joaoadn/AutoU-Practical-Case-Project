import os
from pathlib import Path
from dotenv import load_dotenv

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar variáveis de ambiente do arquivo .env
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    print(f"Aviso: Arquivo .env não encontrado em {ENV_PATH}. Certifique-se de que ele existe.")

# Função para validar variáveis de ambiente obrigatórias
def get_env_variable(name, default=None):
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Variável de ambiente '{name}' não encontrada. Verifique o arquivo .env.")
    return value

# Chave da API da OpenAI (obrigatória)
OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")

# Caminho para o modelo de classificação
MODEL_PATH = os.path.join(BASE_DIR, "models/email-classifier/model.joblib")

# Configurações do Flask
FLASK_CONFIG = {
    "DEBUG": get_env_variable("FLASK_DEBUG", "False") == "True",
    "SECRET_KEY": get_env_variable("FLASK_SECRET_KEY", "supersecretkey"),
    "MAX_CONTENT_LENGTH": int(get_env_variable("MAX_CONTENT_LENGTH", "5242880")),  # 5 MB em bytes
}

# Outras configurações (opcional)
LOG_LEVEL = get_env_variable("LOG_LEVEL", "INFO")  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)