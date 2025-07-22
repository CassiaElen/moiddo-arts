from ..connection import db

class Enderecos:
    def __init__(
        self,
        id_endereco = None,
        cliente_id = None,
        apelido = None,
        rua = None,
        cep = None,
        logradouro = None,
        numero = None,
        complemento = None,
        bairro = None,
        cidade = None,
        estado = None,
        principal = None
    ):
        self.id_endereco = id_endereco
        self.cliente_id = cliente_id
        self.apelido = apelido
        self.rua = rua
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.principal = principal

    def salvar(self):
        """Método para salvar ou editar o objeto no banco"""
        with db.get_conn() as conn:
            cursor = conn.cursor()
            if self.id_cliente is None:
                cursor.execute(
                    """INSERT INTO enderecos (cliente_id, apelido, rua, cep, logradouro, numero, complemento, bairro, cidade, estado, principal) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        self.cliente_id,
                        self.apelido,
                        self.rua,
                        self.cep,
                        self.logradouro,
                        self.numero,
                        self.complemento,
                        self.bairro,
                        self.cidade,
                        self.estado,
                        self.principal,
                    ),
                )
                conn.commit()
                self.id_cliente = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE cliente SET apelido=?, rua=?, cep=?, logradouro=?, numero=?, complemento=?, bairro=?, cidade=?, estado=?, principal=? WHERE id_endereco=?""",
                    (
                        self.apelido,
                        self.rua,
                        self.cep,
                        self.logradouro,
                        self.numero,
                        self.complemento,
                        self.bairro,
                        self.cidade,
                        self.estado,
                        self.principal,
                        self.id_endereco,
                    ),
                )
                conn.commit()

    def buscar_enderecos(self, cliente_id):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM enderecos WHERE cliente_id = ?",(cliente_id,)
            )    
            return [Enderecos(**dict(row)) for row in cursor.fetchall()]

    def buscar_enderecos_service(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM enderecos WHERE id_enderecos = ?", (self.id_endereco,))
                row = cursor.fetchone()
                if row:
                    self.cliente_id = row["cliente_id"]
                    self.apelido = row["apelido"]
                    self.rua = row["rua"]
                    self.cep = row["cep"]
                    self.logradouro = row["logradouro"]
                    self.numero = row["numero"]
                    self.complemento = row["complemento"]
                    self.bairro = row["bairro"]
                    self.cidade = row["cidade"]
                    self.estado = row["estado"]
                    self.principal = row["principal"]
                    return dict(row)
                return None
        except Exception as e:
            print("Erro ao buscar Endereços:", e)
            return None
        