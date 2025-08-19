from ..connection import db
import sqlite3

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
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if self.id_carrinho is None:
                cursor.execute(
                    """INSERT INTO carrinho (cliente_id, data_criacao) VALUES (?, ?)""",
                    (
                        self.cliente_id,
                        self.data_criacao),
                )
                return 
            
    def buscar_carrinho(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id_carrinho FROM carrinho WHERE cliente_id = ?",(self.cliente_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Erro ao buscar carrinho: {e}")
            return False
        
    def deletar_itemCarrinho(self,id_carrinho, id_obra):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM itemCarrinho WHERE carrinho_id = ? AND obra_id = ?", (id_carrinho, id_obra)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao deletar carrinho: {e}")
            return False
    
    def buscar_items_carrinho(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        o.id_obra AS id_obra,
                        o.titulo AS nome_obra,
                        o.preco AS preco,
                        ic.quantidade AS quantidade,
                        (o.preco * ic.quantidade) AS subtotal,
                        o.url_foto AS imagem_url,
                        a.nome_completo AS nome_artista
                    FROM ItemCarrinho ic
                    JOIN carrinho c ON ic.carrinho_id = c.id_carrinho
                    JOIN obras o ON ic.obra_id = o.id_obra
                    JOIN artistas a ON o.artista_id = a.id_artista
                    WHERE c.cliente_id = ?
                """,(self.cliente_id,))
                items = [dict(row) for row in cursor.fetchall()]
                return items
        except Exception as e:
            print(f"Erro ao encontrar items no carrinho: {e}")
            return False
        