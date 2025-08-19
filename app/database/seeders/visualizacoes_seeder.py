from ..connection import db
import random

def seed_visualizacoes():
    visualizacoes = []

    for _ in range(800):
        ip = f"{random.randint(0,200)}.{random.randint(0,200)}.{random.randint(0,200)}.{random.randint(0,200)}"
        tipo_user = random.choice(['cliente', 'artista'])
        
        if random.choice([True, False]):
            artista_id = random.randint(1,8)
            obra_id = None
        else:
            artista_id = None
            obra_id = random.randint(1, 25)

        data = f"2025-07-{random.randint(1, 30):02d}"

        visualizacao = (
            artista_id,
            obra_id,
            random.randint(1, 15),  
            tipo_user,
            ip,
            data
        )

        visualizacoes.append(visualizacao)

    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM visualizacoes")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO visualizacoes (artista_id, obra_id, id_visitante, tipo_user, ip_visitante, data_visualizacao) VALUES (?, ?, ?, ?, ?, ?)",
                visualizacoes,
            )
            print("Visualizações iniciais inseridas com sucesso!")
            conn.commit()
        else:
            print("Visualizações já existem no banco, pulando inserção.")