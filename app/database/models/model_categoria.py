from ..connection import db

class Categoria:
    def __init__(self, id_categoria=None, nome_categoria=None, slug=None):
        self.id_categoria = id_categoria
        self.nome_categoria = nome_categoria
        self.slug = slug

    def salvar(self):
        """Método para salvar ou editar o objeto no banco"""
        with db.get_conn() as conn:
            cursor = conn.cursor()
            if self.id_categoria is None:
                cursor.execute(
                    """INSERT INTO categoria (nome_categoria, slug) VALUES (?, ?)""",
                    (
                        self.nome_categoria,
                        self.slug                   ),
                )
                conn.commit()
                self.id_categoria = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE categoria SET nome_categoria=?, slug=? WHERE id_categoria=?""",
                    (
                        self.nome_categoria,
                        self.slug,
                        self.id_categoria
                    ),
                )
                conn.commit()

    def buscar_categoria(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM categoria WHERE id_categoria = ?", (self.id_categoria,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        
    def buscar_todas_categoria(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categoria")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        
    def deletar_categoria(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM categoria WHERE id_categoria = ?", (self.id_categoria,)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao deletar categoria: {e}")
            return False
