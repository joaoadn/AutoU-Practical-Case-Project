import os
from huggingface_hub import hf_hub_download
from config import BASE_DIR

# Exemplo: Baixar um modelo BERT em português
model_path = hf_hub_download(
    repo_id="neuralmind/bert-base-portuguese-cased",
    filename="pytorch_model.bin",
    cache_dir=os.path.join(BASE_DIR, "models/bert-portuguese")
)
print(f"Modelo baixado em: {model_path}")