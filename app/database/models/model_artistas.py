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
        especialidade=None,
        tecnicasMateriais=None,
        total_obras=0
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
        self.especialidade = especialidade
        self.tecnicasMateriais = tecnicasMateriais
        self.total_obras = total_obras

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
                    """UPDATE artistas SET nome_completo=?, usuario=?, email=?, cpf_cnpj=?, url_avatar=?, biografia=?, especialidade=?, tecnicasMateriais=? WHERE id_artista=?""",
                    (
                        self.nome_completo,
                        self.usuario,
                        self.email,
                        self.cpf_cnpj,
                        self.url_avatar,
                        self.biografia,
                        self.especialidade,
                        self.tecnicasMateriais,
                        self.id_artista,
                    ),
                )
                conn.commit()

    def CheckLoginArtist(self, email, senha):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT id_artista as id, email, status_artista as status, url_avatar as avatar
                        FROM artistas 
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
                    """UPDATE artistas SET senha=? WHERE id_artista=?""",
                    (
                        self.senha,
                        self.id_artista,
                    ),
                )
            conn.commit()

    def buscar_artista(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM artistas WHERE id_artista = ?", (self.id_artista,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print("Erro ao buscar artista:", e)
            return None

    def deletar_artista(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE artistas SET status_artista='inativo' WHERE id_artista=?", (self.id_artista,),
            )
            cursor.execute(
                "UPDATE obras SET status_obras = 'inativa' WHERE artista_id = ?",(self.id_artista,)
            )
            conn.commit()

    def desativar_artista(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE artistas SET status_artista='desativado' WHERE id_artista=?", (self.id_artista,),
            )
            cursor.execute(
                "UPDATE obras SET status_obras = 'inativa' WHERE artista_id = ?",(self.id_artista,)
            )
            conn.commit()

    def buscar_artistasHome(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_artista, nome_completo, url_avatar, biografia, especialidade
                FROM artistas
                ORDER BY id_artista ASC
                LIMIT 4
                """
            )
            return [Artistas(**dict(row)) for row in cursor.fetchall()]

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
            
            return cursor.fetchone()[0]

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

    def calcular_percentual_vendas_mes(self) -> tuple[float, float]:

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

            # Tratamento quando o valor passado é zero
            if total_passado == 0:
            # Retorna 0% de variação e o total atual
                return (0.0, total_atual)

            variacao = ((total_atual - total_passado) / total_passado) * 100

            return  (round(variacao, 2), total_atual)

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

    def buscar_obras_ordenadas(self, ordenacao, pagina, por_pagina):
            from .model_obras import Obras
            try:
                with db.get_conn() as conn:
                    cursor = conn.cursor()
                    order_by = ""
                    if ordenacao == "recentes":
                        order_by = " ORDER BY data_cadastro DESC"
                    elif ordenacao == "antigos":
                        order_by = " ORDER BY data_cadastro ASC"
                    elif ordenacao == "alfabetico":
                        order_by = " ORDER BY titulo ASC"
                    elif ordenacao == "menor_preco":
                        order_by = " ORDER BY preco ASC"
                    elif ordenacao == "maior_preco":
                        order_by = " ORDER BY preco DESC"

                    query = f""" 
                        SELECT * FROM obras
                        WHERE status_obras='ativa' AND artista_id = ?
                        {order_by}
                        LIMIT ? OFFSET ?
                    """

                    offset = (pagina - 1) * por_pagina
                    cursor.execute(query, (self.id_artista, por_pagina, offset))
                    obras = [Obras(**dict(row)) for row in cursor.fetchall()]

                    # Contagem total
                    count_query = """
                    SELECT COUNT(*) FROM obras
                    WHERE status_obras='ativa' AND artista_id = ?
                    """
                    cursor.execute(count_query, (self.id_artista,))
                    total = cursor.fetchone()[0]

                    return obras, total
            except Exception as e:
                print(f"Erro ao buscar obras: {e}")
                return [],0

    def buscar_artista_service(self):
        try:
            with db.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM artistas WHERE id_artista = ?", (self.id_artista,))
                row = cursor.fetchone()
                if row:
                    self.nome_completo = row["nome_completo"]
                    self.usuario = row["usuario"]
                    self.email = row["email"]
                    self.cpf_cnpj = row["cpf_cnpj"]
                    self.senha = row["senha"]
                    self.status_artista = row["status_artista"]
                    self.url_avatar = row["url_avatar"]
                    self.biografia = row["biografia"]
                    return dict(row)
                return None
        except Exception as e:
            print("Erro ao buscar artista:", e)
            return None

    def buscar_pedidos_filtrados(self, status, pagina, por_pagina):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            
            # Base da query
            query = """
                SELECT p.id_pedido, p.data_criacao, p.status_pedido, p.total_pedido, p.entregue,
                    c.nome_completo AS cliente_nome, c.email AS cliente_email, c.url_avatar AS cliente_avatar,
                    o.titulo, ip.quantidade
                FROM pedido p
                JOIN carrinho ca ON ca.id_carrinho = p.carrinho_id
                JOIN cliente c ON ca.cliente_id = c.id_cliente
                JOIN ItemPedido ip ON p.id_pedido = ip.pedido_id
                JOIN obras o ON ip.obra_id = o.id_obra
                WHERE o.artista_id = ?
            """
            params = [self.id_artista]

            # Filtro por status
            if status != "todos":
                query += " AND p.status_pedido = ?"
                params.append(status)

            # Ordenação e paginação
            query += " GROUP BY p.id_pedido ORDER BY p.data_criacao DESC LIMIT ? OFFSET ?"
            offset = (pagina - 1) * por_pagina
            params.extend([por_pagina, offset])

            cursor.execute(query, params)
            pedidos = [dict(row) for row in cursor.fetchall()]

            # Query separada para total de resultados (sem LIMIT/OFFSET)
            count_query = """
                SELECT COUNT(DISTINCT p.id_pedido)
                FROM pedido p
                JOIN carrinho ca ON ca.id_carrinho = p.carrinho_id
                JOIN ItemPedido ip ON p.id_pedido = ip.pedido_id
                JOIN obras o ON ip.obra_id = o.id_obra
                WHERE o.artista_id = ?
            """
            count_params = [self.id_artista]

            if status != "todos":
                count_query += " AND p.status_pedido = ?"
                count_params.append(status)

            cursor.execute(count_query, count_params)
            total = cursor.fetchone()[0]

            return pedidos, total

    def historico_vendas(self,pagina, por_pagina):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            offset = (pagina - 1) * por_pagina
            cursor.execute("""
                SELECT p.id_pedido, p.data_criacao, p.status_pedido, ip.preco, o.titulo
                FROM pedido p
                JOIN carrinho ca ON ca.id_carrinho = p.carrinho_id
                JOIN ItemPedido ip ON p.id_pedido = ip.pedido_id
                JOIN obras o ON ip.obra_id = o.id_obra
                WHERE o.artista_id = ? 
                AND p.status_pedido = 'finalizado'
                ORDER BY p.data_criacao DESC, p.id_pedido
                LIMIT ? OFFSET ?
            """, (self.id_artista, por_pagina, offset))

            vendas = [dict(row) for row in cursor.fetchall()]

            # Contagem total
            count_query = """
                SELECT COUNT(*) FROM pedido p
                JOIN carrinho ca ON ca.id_carrinho = p.carrinho_id
                JOIN ItemPedido ip ON p.id_pedido = ip.pedido_id
                JOIN obras o ON ip.obra_id = o.id_obra
                WHERE status_pedido='finalizado' AND artista_id = ?
                """
            cursor.execute(count_query, (self.id_artista,))
            total = cursor.fetchone()[0]
        return vendas, total

    def to_dict(self):
        return {
            'id_artista': self.id_artista,
            'nome_completo': self.nome_completo,
            'usuario': self.usuario,
            'email': self.email,
            'url_avatar': self.url_avatar,
            'biografia': self.biografia,
            'data_cadastro': self.data_cadastro,
            'total_obras': self.total_obras
        }

    def buscar_artistas_comunidade(self, busca='', filtro='todos', ordenacao='recentes', pagina=1, por_pagina=9):
        #INTEGRAR SISTEMA DE AVALIAÇÃO SE POSSIVEL
        query = """
            SELECT 
                artistas.*,
                (SELECT COUNT(*) FROM obras WHERE artista_id = artistas.id_artista AND status_obras = 'ativa') AS total_obras
            FROM artistas
            WHERE status_artista = 'ativo'
        """
        params = []

        if busca:
            query += " AND (nome_completo LIKE ? OR usuario LIKE ? OR biografia LIKE ?)"
            params.extend([f"%{busca}%"] * 3)

        if ordenacao == 'recentes':
            query += " ORDER BY data_cadastro DESC"
        elif ordenacao == 'antigos':
            query += " ORDER BY data_cadastro ASC"
        elif ordenacao == 'alfabetico':
            query += " ORDER BY nome_completo ASC"
        elif ordenacao == 'mais_obras':
            query += " ORDER BY total_obras DESC"

        offset = (pagina - 1) * por_pagina
        query += " LIMIT ? OFFSET ?"
        params.extend([por_pagina, offset])

        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [Artistas(**dict(row)) for row in cursor.fetchall()]

    def contar_artistas_comunidade(self, busca='', filtro='todos'):
        query = "SELECT COUNT(*) FROM artistas WHERE status_artista = 'ativo'"
        params = []

        if busca:
            query += " AND (nome_completo LIKE ? OR usuario LIKE ? OR biografia LIKE ?)"
            params.extend([f"%{busca}%"] * 3)

        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()[0]
