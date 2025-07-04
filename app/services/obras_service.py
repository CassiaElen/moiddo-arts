from flask import flash
from datetime import datetime
from ..database.models.model_obras import Obras

class ObraService:
    def __init__(self, id_obra=None):
        self.obra = Obras(id_obra=id_obra)
        if id_obra:
            self.obra.buscar_obra_service()
    
    def salvar_obra(self, campos, nome_arquivo):
        salvar_obra = Obras(
            artista_id=1,  # ← session ou login
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
        salvar_obra.salvar()
        
    def editar_obra(self, campos, nome_arquivo):
        if not nome_arquivo:
            self.obra.id_obra = campos['id_obra']
            obra_atual = self.obra.buscar_obra()
            nome_arquivo = obra_atual['url_foto'] if obra_atual else None

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

    def excluir_obra(self, id):
        deletar_obra = Obras(id_obra=id)
        deletar_obra.deletar_obra()
        return flash("Obra deletada com sucesso!", "alert-success")

service_obras = ObraService()
