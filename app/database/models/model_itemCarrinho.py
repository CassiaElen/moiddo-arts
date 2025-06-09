from ..connection import db

class ItemCarrinho:
    def __init__(
        self,
        id_itemCarrinho=None,
        carrinho_id=None,
        obra_id=None,
        preco=None,
        data_adicao=None,
    ):
        self.id_itemCarrinho = id_itemCarrinho
        self.carrinho_id = carrinho_id
        self.obra_id = obra_id
        self.preco = preco
        self.data_adicao = data_adicao
