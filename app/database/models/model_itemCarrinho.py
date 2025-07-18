from ..connection import db

class ItemCarrinho:
    def __init__(
        self,
        id_itemCarrinho=None,
        carrinho_id=None,
        obra_id=None,
        preco=None,
        data_adicao=None,
        quantidade=None
    ):
        self.id_itemCarrinho = id_itemCarrinho
        self.carrinho_id = carrinho_id
        self.obra_id = obra_id
        self.preco = preco
        self.data_adicao = data_adicao
        self.quantidade = quantidade

    def salvar(self):
            """Método para salvar ou editar o objeto no banco"""
            with db.get_conn() as conn:
                cursor = conn.cursor()
                if self.id_itemCarrinho is None:
                    cursor.execute(
                        """INSERT INTO ItemCarrinho (carrinho_id, obra_id, preco, data_adicao, quantidade) VALUES (?, ?,?,?,?)""",
                        (
                            self.carrinho_id,
                            self.obra_id,
                            self.preco,
                            self.data_adicao,
                            self.quantidade
                        ),
                    )
                    conn.commit()
                    self.id_itemCarrinho = cursor.lastrowid
                else:
                    cursor.execute(
                        """UPDATE ItemCarrinho SET preco=? WHERE id_itemCarrinho=?""",
                        (
                            self.preco,
                            self.id_itemCarrinho
                        ),
                    )
                    conn.commit()

    def buscar_itemCarrinho(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM ItemCarrinho WHERE id_itemCarrinho = ?", (self.id_itemCarrinho,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        
    def deletar_categoria(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM ItemCarrinho WHERE id_categoria = ?", (self.id_itemCarrinho,)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao deletar Item do carrinho: {e}")
            return False
