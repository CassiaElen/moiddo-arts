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
    
    def buscar_obrasHome(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM obras WHERE status_obras='ativa' ORDER BY id_obra DESC LIMIT 4")
            rows = cursor.fetchall() 
            return [dict(row) for row in rows]

    def buscar_obras_recomendacoes(self):
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM obras WHERE status_obras='ativa' AND categoria_id = ? AND id_obra NOT IN (?) ORDER BY id_obra DESC LIMIT 3", (self.categoria_id, self.id_obra,)
                )
            rows = cursor.fetchall() 
            return [dict(row) for row in rows]

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

    def buscar_obras_filtradas(self, busca='', filtro='', ordenacao='recentes', pagina=1, por_pagina=9, preco_maximo=None):
        query = """
            SELECT * FROM obras WHERE status_obras = 'ativa'
        """
        params = []

        count_query = """ 
            SELECT COUNT(*) FROM obras WHERE status_obras = 'ativa'
        """
        count_params = []

        if filtro:
            query += f" AND categoria_id = {filtro}"
            
            count_query += f" AND categoria_id = {filtro}"

        if busca:
            query += " AND (titulo LIKE ? OR tecnica LIKE ? OR descricao LIKE ?)"
            params.extend([f"%{busca}%"] * 3)

            count_query += " AND (titulo LIKE ? OR tecnica LIKE ? OR descricao LIKE ?)"
            count_params.extend([f"%{busca}%"] * 3)
        
        if preco_maximo:
            query += " AND preco <= ?"
            params.append(float(preco_maximo))
            
            count_query += " AND preco <= ?"
            count_params.append(float(preco_maximo))

        # Correção na ordenação por preço
        if ordenacao == 'recentes':
            query += " ORDER BY data_cadastro DESC"
        elif ordenacao == 'antigos':
            query += " ORDER BY data_cadastro ASC"
        elif ordenacao == 'alfabetico':
            query += " ORDER BY titulo ASC"
        elif ordenacao == 'menor_preco':
            query += " ORDER BY preco ASC"  # Corrigido de total_obras para preco
        elif ordenacao == 'maior_preco':
            query += " ORDER BY preco DESC"  # Corrigido de total_obras para preco

        offset = (pagina - 1) * por_pagina
        query += " LIMIT ? OFFSET ?"
        params.extend([por_pagina, offset])
        
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            obras = [Obras(**dict(row)) for row in cursor.fetchall()]

            cursor.execute(count_query, count_params)
            total = cursor.fetchone()[0]

            return obras, total        
    def to_dict(self):
        try:
            preco = float(self.preco) if self.preco is not None else None
            
            return {
                'id_obra': self.id_obra,
                'titulo': self.titulo,
                'descricao': self.descricao,
                'tecnica': self.tecnica,
                'dimensoes': self.dimensoes,
                'preco': preco,
                'ano_criacao': self.ano_criacao,
                'estoque': self.estoque,
                'url_foto': self.url_foto
            }
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter obra para dicionário: {e}")
            return None
