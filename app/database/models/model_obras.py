from ..connection import db

class Obras:
    def __init__(
        self,
        id_obra=None,
        titulo=None,
        artista_id=None,
        descricao=None,
        tecnica=None,
        dimensoes=None,
        preco=None,
        categoria_id=None,
        url_foto=None,
        status_obras=None,
        estoque=None,
        ano_criacao=None,
        data_cadastro=None,
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
        self.data_cadastro = data_cadastro

    def salvar(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            if self.id_obra:
                cursor.execute(
                    """
                    UPDATE obras SET
                        artista_id = ?, titulo = ?, descricao = ?, tecnica = ?, dimensoes = ?,
                        preco = ?, categoria_id = ?, url_foto = ?, status_obras = ?, estoque = ?, ano_criacao = ?
                    WHERE id_obra = ?
                """,
                    (
                        self.artista_id,
                        self.titulo,
                        self.descricao,
                        self.tecnica,
                        self.dimensoes,
                        self.preco,
                        self.categoria_id,
                        self.url_foto,
                        self.status_obras,
                        self.estoque,
                        self.ano_criacao,
                        self.id_obra,
                    ),
                )
                conn.commit()
            else:
                cursor.execute(
                    """
                    INSERT INTO obras (
                        artista_id, titulo, descricao, tecnica, dimensoes, preco, categoria_id,
                        url_foto, status_obras, estoque, ano_criacao, data_cadastro
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        self.artista_id,
                        self.titulo,
                        self.descricao,
                        self.tecnica,
                        self.dimensoes,
                        self.preco,
                        self.categoria_id,
                        self.url_foto,
                        self.status_obras,
                        self.estoque,
                        self.ano_criacao,
                        self.data_cadastro
                    ),
                )
                self.id_obra = cursor.lastrowid
                conn.commit()

    def buscar_obra(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM obras WHERE id_obra = ?", (self.id_obra,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def buscar_todas(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM obras WHERE status_obras='ativa'")
            row = cursor.fetchone()
            return dict(row) if row else None
        
    def deletar_obra(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM obras WHERE id_obra = ?", (self.id_obra,)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao deletar obra: {e}")
            return False

    def buscar_obra_service(self):
            try:
                with db.get_conn() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM obras WHERE id_obra = ?", (self.id_obra,))
                    row = cursor.fetchone()
                    if row:
                        self.artista_id = row["artista_id"]
                        self.titulo = row["titulo"]
                        self.descricao = row["descricao"]
                        self.dimensoes = row["dimensoes"]
                        self.preco = row["preco"]
                        self.categoria_id = row["categoria_id"]
                        self.url_foto = row["url_foto"]
                        self.biografia = row["biografia"]
                        self.status_obras = row["status_obras"]
                        self.estoque = row["estoque"]
                        self.ano_criacao = row["ano_criacao"]
                        return dict(row)
                    return None
            except Exception as e:
                print("Erro ao buscar obra:", e)
                return None

    def buscar_categoria(self, categoria):
        with db.get_conn as conn:
            cursor = conn.cursor()
            query = f""" 
            SELECT * FROM obras
            WHERE 
            """
