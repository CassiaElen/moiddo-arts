from ..connection import db

class Carrinho:
    def __init__(
        self,
        id_carrinho=None,
        cliente_id=None,
        data_criacao=None,
    ):
        self.id_carrinho = id_carrinho
        self.cliente_id = cliente_id
        self.data_criacao = data_criacao

    def salvar(self):
        """Método para salvar ou editar o objeto no banco"""
        with db.get_conn() as conn:
            cursor = conn.cursor()
            if self.id_carrinho is None:
                cursor.execute(
                    """INSERT INTO carrinho (cliente_id, data_criacao) VALUES (?, ?)""",
                    (
                        self.cliente_id,
                        self.data_criacao),
                )
                conn.commit()

    def deletar_carrinho(self):
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