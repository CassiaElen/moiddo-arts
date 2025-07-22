from ..database.models.model_enderecos import Enderecos

class EnderecosService:
    def __init__(self, id_endereco=None):
        self.endereco = Enderecos(id_endereco=id_endereco)
        if id_endereco:
            self.endereco.buscar_enderecos_service()
    
    def buscar_enderecos(self, cliente_id):
        return self.endereco.buscar_enderecos(cliente_id)