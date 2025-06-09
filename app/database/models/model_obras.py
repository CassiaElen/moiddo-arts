from ..connection import db

class Obras:
    """Representa um produto no marketplace
    
    Attributes:
        id: Identificador único
        name: Nome do produto
        price: Preço em BRL
        seller_id: ID do vendedor
        is_active: Se está disponível para venda
    """
    def __init__(
        self,
        id_obra=None,
        artista_id=None,
        titulo=None,
        descricao=None,
        tecnica=None,
        dimensoes=None,
        preco=None,
        categoria_id=None,
        url_foto=None,
        status_obras=None,
        estoque=None,
        ano_criacao=None,
    ):
        self.id_obra = id_obra
        self.artista_id = artista_id
        self.titulo = titulo
        self.descricao = descricao
        self.tecnica = tecnica
        self.dimensoes = dimensoes
        self.preco = preco
        self.categoria_id = categoria_id
        self.url_foto = url_foto
        self.status_obras = status_obras
        self.estoque = estoque
        self.ano_criacao = ano_criacao
