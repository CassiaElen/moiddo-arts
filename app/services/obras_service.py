from flask import flash
from datetime import datetime
from ..database.models.model_obras import Obras
from ..services.authmanager import auth_manager 

class ObraService:
    def __init__(self, id_obra=None):
        self.obra = Obras(id_obra=id_obra)
        if id_obra:
            self.obra.buscar_obra_service()
    
    def salvar_obra(self, campos, nome_arquivo):
        user_id = auth_manager.get_current_user_id()
        if user_id is None:
            raise Exception("Usuário não autenticado")
        salvar_obra = Obras(
            artista_id=user_id,
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
        user_id = auth_manager.get_current_user_id()
        if user_id is None:
            raise Exception("Usuário não autenticado")
        
        if not nome_arquivo:
            self.obra.id_obra = campos['id_obra']
            obra_atual = self.obra.buscar_obra()
            nome_arquivo = obra_atual['url_foto'] if obra_atual else None

        editar_obra = Obras(
            artista_id=user_id,  # session ou login
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

    def buscar_obra(self):
        return self.obra.buscar_obra()

    def buscar_obrasHome(self):
        buscar_obras = Obras()
        return buscar_obras.buscar_obrasHome()

    def buscar_obras_recomendacoes(self):
        return self.obra.buscar_obras_recomendacoes()

    def excluir_obra(self, id):
        deletar_obra = Obras(id_obra=id)
        deletar_obra.deletar_obra()
        return flash("Obra deletada com sucesso!", "alert-success")

    def buscar_obras_filtradas(self, busca, filtro, ordenacao, pagina, por_pagina, preco_maximo):
        return self.obra.buscar_obras_filtradas(busca, filtro, ordenacao, pagina, por_pagina, preco_maximo)

