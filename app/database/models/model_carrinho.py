from ..connection import db

class Carrinho:
    def __init__(
        self,
        id_carrinho=None,
        cliente_id=None,
        sessao_id=None,
        status_carrinho=None,
        qtd_item=None,
        data_criacao=None,
    ):
        self.id_carrinho = id_carrinho
        self.cliente_id = cliente_id
        self.sessao_id = sessao_id
        self.status_carrinho = status_carrinho
        self.qtd_item = qtd_item
        self.data_criacao = data_criacao
