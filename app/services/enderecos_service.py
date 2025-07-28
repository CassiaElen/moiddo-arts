from ..database.models.model_enderecos import Enderecos
from ..services.authmanager import auth_manager 
import json

class EnderecosService:
    def __init__(self, id_endereco=None):
        self.endereco = Enderecos(id_endereco=id_endereco)
        if id_endereco:
            self.endereco.buscar_enderecos_service()
    
    def buscar_enderecos(self, cliente_id):
        return self.endereco.buscar_enderecos(cliente_id)
    
    def editar_enderecos(self, campos):
        user_id = auth_manager.get_current_user_id()
        if user_id is None:
            raise Exception("Usuário não autenticado")

        editar_endereco = Enderecos(
            cliente_id = user_id,
            apelido = campos["apelido"],
            rua = campos["rua"],
            cep = campos["cep"],
            logradouro = campos["logradouro"],
            numero = campos["numero"],
            complemento = campos["complemento"],
            bairro = campos["bairro"],
            cidade = campos["cidade"],
            estado = campos["estado"],
            #principal = principal,
            id_endereco=campos["id_endereco"]
        )

        
        editar_endereco.salvar()
        campos = json.loads(campos)