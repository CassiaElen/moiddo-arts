from ..connection import db

class Pedido:
    def __init__(
        self,
        id_pedido=None,
        carrinho_id=None,
        cliente_id=None,
        status_pedido=None,
        entregue=None,
        total_pedido=None,
        data_criacao=None,
    ):
        self.id_pedido = id_pedido
        self.carrinho_id = carrinho_id
        self.cliente_id = cliente_id
        self.status_pedido = status_pedido
        self.entregue = entregue
        self.total_pedido = total_pedido
        self.data_criacao = data_criacao

