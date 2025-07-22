from ..connection import db

class Cliente:
    def __init__(
        self,
        id_cliente=None,
        nome_completo=None,
        usuario=None,
        email=None,
        telefone = None,
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
        self.telefone = telefone
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
                    """INSERT INTO cliente (nome_completo, usuario, email, telefone, cpf, senha, data_cadastro) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        self.nome_completo,
                        self.usuario,
                        self.email,
                        self.telefone,
                        self.cpf,
                        self.senha,
                        self.data_cadastro,
                    ),
                )
                conn.commit()
                self.id_cliente = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE cliente SET nome_completo=?, usuario=?, email=?, telefone=?, cpf=?, url_avatar=? WHERE id_cliente=?""",
                    (
                        self.nome_completo,
                        self.usuario,
                        self.email,
                        self.telefone,
                        self.cpf,
                        self.url_avatar,
                        self.id_cliente,
                    ),
                )
                conn.commit()

    def CheckLoginClient(self, email, senha):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT id_cliente as id, email, senha, status_cliente as status, url_avatar as avatar
                        FROM cliente 
                        WHERE email=? AND senha=?
                        """,
                        (
                            email,
                            senha
                        ))
            row = cursor.fetchone()
            if not row:
                return None
        
            return {
                'id': row['id'],
                'email': row['email'],
                'status': row['status'],
                'avatar': row['avatar']
            }

    def editar_senha(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                    """UPDATE cliente SET senha=? WHERE id_cliente=?""",
                    (
                        self.senha,
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
                        "DELETE FROM cliente WHERE id_cliente = ?", (self.id_cliente,)
                    )
                    conn.commit()
                    return True
            except Exception as e:
                print(f"Erro ao deletar cliente: {e}")
                return False

    def buscar_cliente_service(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM cliente WHERE id_cliente = ?", (self.id_cliente,))
                row = cursor.fetchone()
                if row:
                    self.nome_completo = row["nome_completo"]
                    self.usuario = row["usuario"]
                    self.email = row["email"]
                    self.cpf = row["cpf"]
                    self.telefone = row["telefone"]
                    self.senha = row["senha"]
                    self.status_cliente = row["status_cliente"]
                    self.url_avatar = row["url_avatar"]
                    return dict(row)
                return None
        except Exception as e:
            print("Erro ao buscar cliente:", e)
            return None
