from flask import request
from ..services.authmanager import auth_manager

def tratar_visualizacao(artista_id, obra_id):

    ip = request.remote_addr

    from ..services.visualizacao_service import VisualizacaoService
    service_visualizacoes = VisualizacaoService()

    service_visualizacoes.registrar(
        artista_id=artista_id, 
        obra_id=obra_id, 
        id_visitante=auth_manager.get_current_user_id(), 
        tipo_user=auth_manager.current_user_type(), 
        ip_visitante=ip
    )