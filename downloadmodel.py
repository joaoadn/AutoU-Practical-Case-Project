from huggingface_hub import snapshot_download

# Baixa o modelo completo para uma pasta local
model_path = snapshot_download(
    repo_id="neuralmind/bert-base-portuguese-cased",
    local_dir="./models/bert-portuguese",  # Pasta onde o modelo será salvo
    local_dir_use_symlinks=False  # Evita problemas com symlinks no Windows
)
print(f"Modelo baixado para: {model_path}")