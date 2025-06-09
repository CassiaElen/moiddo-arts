from ..database.models.model_artistas import Artistas
class ArtistaService:
    
    @staticmethod
    def dados_artista():
        artista = Artistas(id_artista=1)
        dados_artista = artista.buscar_artista()
        return dados_artista
    #@staticmethod
    # def salvar_dados():
        
service_artistas = ArtistaService()