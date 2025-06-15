from ..database.models.model_artistas import Artistas

class ArtistaService:
    def __init__(self, id_artista=None):
        self.artista = Artistas(id_artista=id_artista)

    def dados_artista(self):
        return self.artista.buscar_artista()

    def contar_obras(self):
        return self.artista.contar_obras()

    def contar_obras_mes(self):
        return self.artista.contar_obras_mes_atual()

    def ultimas_obras(self):
        return self.artista.buscar_ultimas_obras()

    def contar_total_vendas(self):
        return self.artista.calcular_total_vendas()

    def contar_porcentagem_vendas(self):
        return self.artista.calcular_percentual_vendas_mes()
    
    def buscar_obras_filtradas(self, busca, filtro, pagina, por_pagina):
        return self.artista.buscar_obras_filtradas(busca, filtro, pagina, por_pagina )


service_artistas = ArtistaService(id_artista=1)