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

    def salvar(self):
        """Método para salvar ou editar o objeto no banco"""
        with db.get_conn() as conn:
            cursor = conn.cursor()
            if self.id_carrinho is None:
                cursor.execute(
                    """NSERT INTO carrinho (cliente_id, sessao_id, status_carrinho, qtd_item, data_criacao)
                VALUES (?, NULL, 'ativo', 0, ?)""",
                    (
                        self.cliente_id,
                        self.sessao_id,
                        self.status_carrinho,
                        self.qtd_item,
                        self.data_criacao                    ),
                )
                conn.commit()
                self.id_carrinho = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE carrinho SET status_carrinho=?, qtd_item=? WHERE id_carrinho=?""",
                    (
                        self.status_carrinho,
                        self.qtd_item,
                        self.id_carrinho
                    ),
                )
                conn.commit()

    def buscar_carrinho(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM carrinho WHERE id_carrinho = ?", (self.id_carrinho,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        
    def deletar_cliente(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM carrinho WHERE id_carrinho = ?", (self.id_carrinho,)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao deletar carrinho: {e}")
            return False