from datetime import datetime
from ..database.connection import db
from ..database.models.model_obras import Obras

class ObraService:
    
    def salvar_obra(self, campos, nome_arquivo):
        nova_obra = Obras(
            artista_id=1,  # ← idealmente isso vem do session ou login
            titulo=campos["titulo"],
            descricao=campos["descricao"],
            tecnica=campos["tecnica"],
            dimensoes=campos["dimensao"],
            preco=float(campos["preco"]),
            categoria_id=int(campos["categoria"]),
            url_foto=nome_arquivo,
            status_obras=campos["status"],
            estoque=int(campos["estoque"]),
            ano_criacao=int(campos["ano"]),
            data_cadastro=datetime.now().strftime("%Y-%m-%d")
        )
        nova_obra.salvar()

    def editar_obra(self, campos, nome_arquivo):
        editar_obra = Obras(
            artista_id=1,  # session ou login
            titulo=campos["titulo"],
            descricao=campos["descricao"],
            tecnica=campos["tecnica"],
            dimensoes=campos["dimensao"],
            preco=float(campos["preco"]),
            categoria_id=int(campos["categoria"]),
            url_foto=nome_arquivo,
            status_obras=campos["status"],
            estoque=int(campos["estoque"]),
            ano_criacao=int(campos["ano"]),
            id_obra=campos['id_obra']
        )
        editar_obra.salvar()


service_obras = ObraService()
