from ..connection import db


class Artistas:
    def __init__(
        self,
        id_artista=None,
        nome_completo=None,
        usuario=None,
        email=None,
        cpf_cnpj=None,
        senha=None,
        status_artista="ativo",
        data_cadastro=None,
        url_avatar=None,
        biografia=None,
    ):
        self.id_artista = id_artista
        self.nome_completo = nome_completo
        self.usuario = usuario
        self.email = email
        self.cpf_cnpj = cpf_cnpj
        self.senha = senha
        self.status_artista = status_artista
        self.data_cadastro = data_cadastro
        self.url_avatar = url_avatar
        self.biografia = biografia

    def salvar(self):
        """Método para salvar ou editar o objeto no banco"""
        with db.get_conn() as conn:
            cursor = conn.cursor()
            if self.id_artista is None:
                cursor.execute(
                    """INSERT INTO artistas (nome_completo, usuario, email, cpf_cnpj, senha, data_cadastro) VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        self.nome_completo,
                        self.usuario,
                        self.email,
                        self.cpf_cnpj,
                        self.senha,
                        self.data_cadastro,
                    )
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE artistas SET nome_completo=?, usuario=?, email=?, cpf_cnpj=?, senha=? WHERE id_artista=?""",
                    (
                        self.nome_completo,
                        self.usuario,
                        self.email,
                        self.cpf_cnpj,
                        self.senha,
                        self.id_artista
                    )
                )
                conn.commit()

    def buscar_obras(self):
        from .model_obras import Obras
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM obras WHERE artista_id = ?",(self.id_artista,))
            return [Obras(**dict(row)) for row in cursor.fetchall()]

    def buscar_artista(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM artistas WHERE id_artista = ?", (self.id_artista,))
            row = cursor.fetchone()
            return dict(row) if row else None


