from ..connection import db

class Cliente:
    def __init__(
        self,
        id_cliente=None,
        nome_completo=None,
        usuario=None,
        email=None,
        cpf=None,
        senha=None,
        status_cliente=None,
        data_cadastro=None,
        url_avatar=None,
    ):
        self.id_cliente = id_cliente
        self.nome_completo = nome_completo
        self.usuario = usuario
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.status_cliente = status_cliente
        self.data_cadastro = data_cadastro
        self.url_avatar = url_avatar

    def salvar(self):
        """Método para salvar ou editar o objeto no banco"""
        with db.get_conn() as conn:
            cursor = conn.cursor()
            if self.id_cliente is None:
                cursor.execute(
                    """INSERT INTO clinte (nome_completo, usuario, email, cpf, senha, data_cadastro) VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        self.nome_completo,
                        self.usuario,
                        self.email,
                        self.cpf,
                        self.senha,
                        self.data_cadastro,
                    ),
                )
                conn.commit()
                self.id_cliente = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE cliente SET nome_completo=?, usuario=?, email=?, cpf=?, senha=?, status_cliente=?, url_avatar=? WHERE id_cliente=?""",
                    (
                        self.nome_completo,
                        self.usuario,
                        self.email,
                        self.cpf,
                        self.senha,
                        self.status_cliente,
                        self.url_avatar,
                        self.id_cliente,
                    ),
                )
                conn.commit()

    def buscar_cliente(self):
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM cliente WHERE id_cliente = ?", (self.id_cliente,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
            
    def deletar_cliente(self):
            try:
                with db.get_conn() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM clientes WHERE id_cliente = ?", (self.id_cliente,)
                    )
                    conn.commit()
                    return True
            except Exception as e:
                print(f"Erro ao deletar cliente: {e}")
                return False