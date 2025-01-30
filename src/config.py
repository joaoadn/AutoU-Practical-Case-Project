import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar variáveis de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_PATH = os.path.join(BASE_DIR, "models/email-classifier/model.joblib")

# Configurações do Flask
FLASK_CONFIG = {
    "DEBUG": os.getenv("FLASK_DEBUG", "False") == "True",
    "SECRET_KEY": os.getenv("FLASK_SECRET_KEY", "supersecretkey"),
}