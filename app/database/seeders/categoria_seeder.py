from ..connection import db

# Popula a tabela de categorias com dados iniciais
def seed_categorias():
    categorias = [
        ("Xilogravura", "xilogravura"),
        ("Escultura em Barro", "escultura-em-barro"),
        ("Escultura em Madeira", "escultura-em-madeira"),
        ("Pintura", "pintura"),
        ("Ilustração Digital", "ilustracao-digital"),
        ("Artesanato Têxtil", "artesanato-textil"),
        ("Bijuterias e Acessórios Artesanais", "bijuterias-acessorios-artesanais"),
        ("Cerâmica", "ceramica"),
        ("Cordel e Literatura Visual", "cordel-literatura-visual"),
        ("Fotografia Artística", "fotografia-artistica"),
        ("Arte Reciclada", "arte-reciclada"),
        ("Arte Popular", "arte-popular"),
    ]

    with db.get_conn() as conn:
        cursor = conn.cursor()
        # Verifica se já existem categorias para não duplicar
        cursor.execute("SELECT COUNT(*) FROM categoria")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO categoria (nome_categoria, slug) VALUES (?, ?)", categorias
            )
            print("Categorias iniciais inseridas com sucesso!")
            conn.commit()
        else:
            print("Categorias já existem no banco, pulando inserção.")
