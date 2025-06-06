from ..connection import db

class Artistas:
    def __init__(
        self,
        id_artista=None,
        nome_completo=None,
        usuario=None,
        email=None,
        cpf_cnpj=None,
        senha=None,
        status_artista="ativo",
        data_cadastro=None,
        url_avatar=None,
        biografia=None,
    ):
        self.id_artista = id_artista
        self.nome_completo = nome_completo
        self.usuario = usuario
        self.email = email
        self.cpf_cnpj = cpf_cnpj
        self.senha = senha
        self.status_artista = status_artista
        self.data_cadastro = data_cadastro
        self.url_avatar = url_avatar
        self.biografia = biografia

    def registrar(self):
        """Método básico para salvar o objeto no banco"""
