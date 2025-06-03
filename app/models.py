import sqlite3

def tabela_artistas():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS artistas(
            id_artista INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            cpf_cnpj VARCHAR(18) UNIQUE NOT NULL,
            senha VARCHAR(100) NOT NULL,
            data_cadastro DATETIME NOT NULL,
            url_avatar VARCHAR(100),
            biografia VARCHAR(200)
    )
"""
    cursor.execute(sql)
    con.commit()
    con.close()

def tabela_compradores():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS comprador(
            id_comprador INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            cpf VARCHAR(18) UNIQUE NOT NULL,
            senha VARCHAR(100) NOT NULL,
            data_cadastro DATETIME NOT NULL,
            url_avatar VARCHAR(100)
    )
"""
    cursor.execute(sql)
    con.commit()
    con.close()

def tabela_categorias():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS categoria(
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_categoria VARCHAR(100) NOT NULL,
            slug VARCHAR(50) UNIQUE NOT NULL
    )
    """
    cursor.execute(sql)
    con.commit()
    con.close()

def tabela_obras():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS obras(
            id_obra INTEGER PRIMARY KEY AUTOINCREMENT,
            artista_id INTEGER,
            titulo VARCHAR(100) NOT NULL,
            descricao VARCHAR(200) NOT NULL,
            tecnica VARCHAR(100),
            dimensoes VARCHAR(100),
            preco DECIMAL(5,2) NOT NULL,
            categoria_id INTEGER NOT NULL,
            url_foto VARCHAR(100),
            FOREIGN KEY(artista_id) REFERENCES artistas(id_artista),
            FOREIGN KEY(categoria_id) REFERENCES categoria(id_categoria)
    )
"""
    cursor.execute(sql)
    con.commit()
    con.close()

def tabela_carrinho():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS carrinho(
            id_carrinho INTEGER PRIMARY KEY AUTOINCREMENT,
            comprador_id INTEGER,
            sessao_id INTEGER,
            status_carrinho VARCHAR(15) DEFAULT 'ativo' CHECK (status_carrinho IN ('ativo','finalizado','cancelado')),
            qtd_item INTEGER NOT NULL,
            data_criacao DATETIME,
            FOREIGN KEY(comprador_id) REFERENCES comprador(id_comprador)
    )
"""
    cursor.execute(sql)
    con.commit()
    con.close()

def tabela_item_carrinho():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS ItemCarrinho(
            id_itemCarrinho INTEGER PRIMARY KEY AUTOINCREMENT,
            carrinho_id INTEGER,
            obra_id INTEGER,
            preco DECIMAL(5,2) NOT NULL,
            data_adicao DATETIME NOT NULL,
            FOREIGN KEY(carrinho_id) REFERENCES carrinho(id_carrinho),
            FOREIGN KEY(obra_id) REFERENCES obras(id_obra)
    )
"""
    cursor.execute(sql)
    con.commit()
    con.close()

def tabela_pedido():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS pedido(
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            carrinho_id INTEGER,
            comprador_id INTEGER,
            status_pedido VARCHAR(15) DEFAULT 'pendente' CHECK (status_pedido IN ('pendente','finalizado','cancelado')),
            total_pedido DECIMAL(5,2) NOT NULL,
            data_criacao DATETIME NOT NULL,
            FOREIGN KEY(carrinho_id) REFERENCES carrinho(id_carrinho),
            FOREIGN KEY(comprador_id) REFERENCES comprador(id_comprador)
    )
"""
    cursor.execute(sql)
    con.commit()
    con.close()

def tabela_item_pedido():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS ItemPedido(
            id_itemPedido INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER,
            obra_id INTEGER,
            preco DECIMAL(5,2) NOT NULL,
            FOREIGN KEY(pedido_id) REFERENCES pedido(id_pedido),
            FOREIGN KEY(obra_id) REFERENCES obras(id_obra)
    )
"""
    cursor.execute(sql)
    con.commit()
    con.close()

tabela_artistas()
tabela_compradores()
tabela_categorias()
tabela_obras()
tabela_carrinho()
tabela_item_carrinho()
tabela_pedido()
tabela_item_pedido()

#popular tabela categoria

"""
def inserir_categorias():
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
        ("Arte Popular", "arte-popular")
    ]
    
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    cursor.executemany("INSERT INTO categoria (nome_categoria, slug) VALUES (?, ?)", categorias)
    con.commit()
    con.close()
"""
def inserir_categorias():
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
        ("Arte Popular", "arte-popular")
    ]
    
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    
    cursor.execute("CREATE TEMPORARY TABLE temp_categorias (nome_categoria TEXT, slug TEXT)")
    cursor.executemany("INSERT INTO temp_categorias (nome_categoria, slug) VALUES (?, ?)", categorias)
    
    cursor.execute("""
        INSERT OR IGNORE INTO categoria (nome_categoria, slug)
        SELECT nome_categoria, slug
        FROM temp_categorias
        WHERE NOT EXISTS (
            SELECT 1
            FROM categoria
            WHERE (nome_categoria = temp_categorias.nome_categoria OR slug = temp_categorias.slug)
        )
    """)
    
    # Remover a tabela temporária
    cursor.execute("DROP TABLE temp_categorias")
    
    con.commit()
    con.close()
inserir_categorias()