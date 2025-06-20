import os
import uuid
from werkzeug.utils import secure_filename

BASE_UPLOAD_FOLDER = "app/static/assets/uploads"

def salvar_imagem(imagem, subpasta="obras"):
    if not imagem or imagem.filename == "":
        return None

    nome_seguro = secure_filename(imagem.filename)
    extensao = os.path.splitext(nome_seguro)[1]
    nome_unico = f"{uuid.uuid4().hex}{extensao}"

    # Caminho completo com subpasta 
    pasta_destino = os.path.join(BASE_UPLOAD_FOLDER, subpasta)
    os.makedirs(pasta_destino, exist_ok=True)  # Garante que a pasta existe

    caminho_completo = os.path.join(pasta_destino, nome_unico)
    imagem.save(caminho_completo)

    # Caminho que será salvo no banco 
    return f"/static/assets/uploads/{subpasta}/{nome_unico}"

