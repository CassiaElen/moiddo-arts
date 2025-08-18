from ..connection import db
import sqlite3

class Visualizacoes:
    def __init__(
        self, 
        id_visualizacao = None,
        artista_id = None,
        obra_id = None,
        id_visitante = None,
        tipo_user = None, 
        ip_visitante = None,
        data_visualizacao = None
    ):
        self.id_visualizacao = id_visualizacao
        self.artista_id = artista_id
        self.obra_id = obra_id
        self.id_visitante = id_visitante
        self.tipo_user = tipo_user
        self.ip_visitante = ip_visitante
        self.data_visualizacao = data_visualizacao

    def registrar(self):
        with db.get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO visualizacoes (artista_id, obra_id, id_visitante, tipo_user, ip_visitante, data_visualizacao) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    self.artista_id,
                    self.obra_id,
                    self.id_visitante,
                    self.tipo_user,
                    self.ip_visitante,
                    self.data_visualizacao,
                ),
            )
            conn.commit()
            self.id_visualizacao = cursor.lastrowid

    def visualizacoes_obra(self, obra_id):
        conn.row_factory = sqlite3.Row
        with db.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM visualizacoes WHERE obra_id = ?", (obra_id,)
            )
            return cursor.fetchone()[0]
    
    def visualizacoes_artista(self, artista_id):
        with db.get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM visualizacoes WHERE obra_id = ?", (artista_id,)
            )
            return cursor.fetchone()[0]

    def buscar_visualizacao_service(self):
        try:
            with db.get_conn() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM visualizacoes WHERE id_visualizacao = ?", (self.id_visualizacao,))
                row = cursor.fetchone()
                if row:
                    self.artista_id = row["artista_id"]
                    self.obra_id = row["obra_id"]
                    self.id_visitante = row["id_visitante"]
                    self.tipo_user = row["tipo_user"]
                    self.ip_visitante = row["ip_visitante"]
                    self.data_visualizacao = row["data_visualizacao"]
                    return dict(row)
                return None
        except Exception as e:
            print("Erro ao buscar visualização:", e)
            return None