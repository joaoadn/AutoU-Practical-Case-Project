import os
from huggingface_hub import snapshot_download
from config import BASE_DIR

# Definir diretório de cache para armazenar modelos
MODEL_DIR = os.path.join(BASE_DIR, "models/xlm-roberta")

# Baixar todos os arquivos necessários do modelo XLM-RoBERTa
model_path = snapshot_download(
    repo_id="xlm-roberta-base",
    cache_dir=MODEL_DIR,
    allow_patterns=["*.bin", "*.json", "*.txt"]  # Baixa apenas arquivos essenciais
)

print(f"Modelo baixado em: {model_path}")

# Créditos:
# - Modelo: XLM-RoBERTa-Base (Hugging Face: https://huggingface.co/xlm-roberta-base)
# - Desenvolvido por: Meta AI (ex-Facebook AI)
# - Código adaptado por [João Dias]