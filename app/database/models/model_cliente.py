from ..connection import db

class Cliente:
    def __init__(
        self,
        id_cliente=None,
        nome_completo=None,
        usuario=None,
        email=None,
        cpf=None,
        senha=None,
        status_cliente=None,
        data_cadastro=None,
        url_avatar=None,
    ):
        self.id_cliente = id_cliente
        self.nome_completo = nome_completo
        self.usuario = usuario
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.status_cliente = status_cliente
        self.data_cadastro = data_cadastro
        self.url_avatar = url_avatar
