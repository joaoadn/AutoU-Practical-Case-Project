from huggingface_hub import snapshot_download
import os
import shutil

# Caminho para salvar o modelo
model_dir = "../models/bert-portuguese"  # Caminho relativo à pasta `src/`

# Verifica se a pasta de modelos existe, caso contrário, cria
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Verifica se há espaço suficiente em disco (mínimo 1GB)
total, used, free = shutil.disk_usage("/")
if free < 1 * 1024 * 1024 * 1024:  # 1GB
    raise OSError("Espaço insuficiente em disco para baixar o modelo.")

# Baixa o modelo completo para a pasta local
try:
    print("Iniciando o download do modelo...")
    model_path = snapshot_download(
        repo_id="neuralmind/bert-base-portuguese-cased",
        local_dir=model_dir,  # Pasta onde o modelo será salvo
        local_dir_use_symlinks=False  # Evita problemas com symlinks no Windows
    )
    print(f"Modelo baixado para: {model_path}")
except Exception as e:
    print(f"Erro ao baixar o modelo: {e}")