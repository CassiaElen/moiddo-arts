from ..database.models.model_visualizacoes import Visualizacoes

class VisualizacaoService:

    def __init__(self, id_visualizacao=None):
        self.visualizacao = Visualizacoes(id_visualizacao=id_visualizacao)
        if id_visualizacao:
            self.visualizacao.buscar_visualizacao_service()
    
    def registrar(self, artista_id, obra_id, id_visitante, tipo_user, ip_visitante):
        from datetime import datetime
        data_visualizacao = datetime.now().strftime("%Y-%m-%d")
        self.visualizacao.artista_id = artista_id
        self.visualizacao.obra_id = obra_id 
        self.visualizacao.id_visitante = id_visitante
        self.visualizacao.tipo_user = tipo_user
        self.visualizacao.ip_visitante = ip_visitante
        self.visualizacao.data_visualizacao = data_visualizacao
        self.visualizacao.registrar()

    def visualizacoes_obra(self, obra_id):
        return self.visualizacao.visualizacoes_obra(obra_id=obra_id)