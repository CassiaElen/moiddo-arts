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
        status_artista=None,
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
                    ),
                )
                conn.commit()
                self.id_artista = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE artistas SET nome_completo=?, usuario=?, email=?, cpf_cnpj=?, senha=?, status_artista=?, url_avatar=?, biografia=? WHERE id_artista=?""",
                    (
                        self.nome_completo,
                        self.usuario,
                        self.email,
                        self.cpf_cnpj,
                        self.senha,
                        self.status_artista,
                        self.url_avatar,
                        self.biografia,
                        self.id_artista,
                    ),
                )
                conn.commit()

    def buscar_artista(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM artistas WHERE id_artista = ?", (self.id_artista,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def deletar_artista(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM artistas WHERE id_artista = ?", (self.id_artista,)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao deletar artista: {e}")
            return False

    def buscar_obras(self):
        from .model_obras import Obras

        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM obras WHERE artista_id = ?", (self.id_artista,)
            )
            return [Obras(**dict(row)) for row in cursor.fetchall()]
    
    def buscar_ultimas_obras(self):
        from .model_obras import Obras

        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM obras
                WHERE artista_id = ?
                ORDER BY data_cadastro DESC
                LIMIT 2
                """,
                (self.id_artista,),
            )
            return [Obras(**dict(row)) for row in cursor.fetchall()]

    def contar_obras(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM obras WHERE artista_id = ?", (self.id_artista,)
            )
            quantidade = cursor.fetchone()[0]
            return quantidade

    def contar_obras_mes_atual(self):
        from datetime import datetime

        now = datetime.now()
        ano = now.year
        mes = now.month

        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) FROM obras 
                WHERE artista_id = ? 
                AND strftime('%Y', data_cadastro) = ? 
                AND strftime('%m', data_cadastro) = ?
                """,
                (self.id_artista, str(ano), f"{mes:02}"),
            )
            return cursor.fetchone()[0]

    def calcular_total_vendas(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    SUM(ip.preco * ip.quantidade) AS total_vendas
                FROM 
                    obras o
                JOIN 
                    ItemPedido ip ON o.id_obra = ip.obra_id
                JOIN 
                    pedido p ON ip.pedido_id = p.id_pedido
                WHERE 
                    o.artista_id = ?
                    AND p.status_pedido = 'finalizado'
            """,
                (self.id_artista,),
            )
            resultado = cursor.fetchone()[0]
            return resultado if resultado else 0.0

    def calcular_percentual_vendas_mes(self):

        from datetime import datetime, timedelta
        with db.get_conn() as conn:
            cursor = conn.cursor()

            # Mês atual
            agora = datetime.now()
            inicio_mes_atual = agora.replace(day=1).strftime('%Y-%m-%d')
            inicio_proximo_mes = (agora.replace(day=28) + timedelta(days=4)).replace(day=1).strftime('%Y-%m-%d')

            # Mês anterior
            inicio_mes_passado = (agora.replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d')
            fim_mes_passado = agora.replace(day=1).strftime('%Y-%m-%d')

            # Vendas mês atual
            cursor.execute("""
                SELECT SUM(ip.preco * ip.quantidade)
                FROM obras o
                JOIN ItemPedido ip ON o.id_obra = ip.obra_id
                JOIN pedido p ON p.id_pedido = ip.pedido_id
                WHERE o.artista_id = ?
                AND p.status_pedido = 'finalizado'
                AND p.data_criacao >= ? AND p.data_criacao < ?
            """, (self.id_artista, inicio_mes_atual, inicio_proximo_mes))
            total_atual = cursor.fetchone()[0] or 0

            # Vendas mês passado
            cursor.execute("""
                SELECT SUM(ip.preco * ip.quantidade)
                FROM obras o
                JOIN ItemPedido ip ON o.id_obra = ip.obra_id
                JOIN pedido p ON p.id_pedido = ip.pedido_id
                WHERE o.artista_id = ?
                AND p.status_pedido = 'finalizado'
                AND p.data_criacao >= ? AND p.data_criacao < ?
            """, (self.id_artista, inicio_mes_passado, fim_mes_passado))
            total_passado = cursor.fetchone()[0] or 0

            if total_passado == 0:
                return 100.0 if total_atual > 0 else 0.0

            variacao = ((total_atual - total_passado) / total_passado) * 100
            return round(variacao, 2)

    def buscar_obras_filtradas(self, busca, filtro, pagina, por_pagina):
            from .model_obras import Obras
            with db.get_conn() as conn:
                cursor = conn.cursor()

                # Base da query
                query = "SELECT * FROM obras WHERE artista_id = ?"
                params = [self.id_artista]

                # Filtro por status
                if filtro == "ativas":
                    query += " AND status_obras = 'ativa'"
                elif filtro == "rascunhos":
                    query += " AND status_obras = 'rascunho'"
                elif filtro == "esgotadas":
                    query += " AND estoque <= 0"

                # Filtro por busca
                if busca:
                    query += " AND (titulo LIKE ? OR tecnica LIKE ?)"
                    like = f"%{busca}%"
                    params.extend([like, like])

                # Ordenação e paginação
                query += " ORDER BY data_cadastro DESC LIMIT ? OFFSET ?"
                offset = (pagina - 1) * por_pagina
                params.extend([por_pagina, offset])

                cursor.execute(query, params)
                obras = [Obras(**dict(row)) for row in cursor.fetchall()]

                # Query separada para total de resultados (sem LIMIT/OFFSET)
                count_query = "SELECT COUNT(*) FROM obras WHERE artista_id = ?"
                count_params = [self.id_artista]

                if filtro == "ativas":
                    count_query += " AND status_obras = 'ativa'"
                elif filtro == "rascunhos":
                    count_query += " AND status_obras = 'rascunho'"
                elif filtro == "esgotadas":
                    count_query += " AND estoque <= 0"

                if busca:
                    count_query += " AND (titulo LIKE ? OR tecnica LIKE ?)"
                    count_params.extend([like, like])

                cursor.execute(count_query, count_params)
                total = cursor.fetchone()[0]

                return obras, total