from ..connection import db

class ItemPedido:
    def __init__(
        self,
        id_itemPedido=None,
        pedido_id=None,
        obra_id=None,
        preco=None,
        data_adicao=None,
    ):
        self.id_itemPedido = id_itemPedido
        self.pedido_id = pedido_id
        self.obra_id = obra_id
        self.preco = preco
        self.data_adicao = data_adicao
