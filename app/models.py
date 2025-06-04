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
            status_artista VARCHAR(15) DEFAULT 'ativo' CHECK (status_artista IN ('ativo','desativado','bloqueado')),
            data_cadastro DATETIME NOT NULL,
            url_avatar VARCHAR(100),
            biografia VARCHAR(200)
    )
"""
    cursor.execute(sql)
    con.commit()
    con.close()

def tabela_cliente():
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS cliente(
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            cpf VARCHAR(18) UNIQUE NOT NULL,
            senha VARCHAR(100) NOT NULL,
            status_cliente VARCHAR(15) DEFAULT 'ativo' CHECK (status_cliente IN ('ativo','desativado','bloqueado')),
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
            status_obras VARCHAR(15) CHECK (status_obras IN ('ativo','rascunho')),
            estoque INTEGER,
            ano_criacao DATETIME,
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
            cliente_id INTEGER,
            sessao_id INTEGER,
            status_carrinho VARCHAR(15) DEFAULT 'ativo' CHECK (status_carrinho IN ('ativo','finalizado','cancelado')),
            qtd_item INTEGER NOT NULL,
            data_criacao DATETIME,
            FOREIGN KEY(cliente_id) REFERENCES cliente(id_cliente)
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
            cliente_id INTEGER,
            status_pedido VARCHAR(15) DEFAULT 'pendente' CHECK (status_pedido IN ('pendente','finalizado','cancelado')),
            total_pedido DECIMAL(5,2) NOT NULL,
            data_criacao DATETIME NOT NULL,
            FOREIGN KEY(carrinho_id) REFERENCES carrinho(id_carrinho),
            FOREIGN KEY(cliente_id) REFERENCES cliente(id_cliente)
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

# popular tabela categoria
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
    
    cursor.execute("DROP TABLE temp_categorias")
    
    con.commit()
    con.close()

def inserir_artistas():
    artistas = [
        ("Ana Beatriz Lima", "anabeatriz", "ana.lima@example.com", "111.222.333-44", "senha789", "ativo", "2023-02-15", "../app/static/assets/perfils/beatriz.jpeg", "Ceramista premiada com obras em museus internacionais"),
        ("Carlos Eduardo Santos", "carlosedu", "carlos.santos@example.com", "222.333.444-55", "senha101", "ativo", "2023-03-10", "../app/static/assets/perfils/carlos.jpg", "Mestre em xilogravura nordestina"),
        ("Fernanda Oliveira", "feoliveira", "fernanda.art@example.com", "333.444.555-66", "senha202", "bloqueado", "2023-04-05", "../app/static/assets/perfils/fernanda.jpg", "Fotógrafa artística com foco em cultura popular"),
        ("Ricardo Almeida", "ricardoarte", "ricardo.a@example.com", "444.555.666-77", "senha303", "ativo", "2023-05-20", "../app/static/assets/perfils/ricardo.jpg", "Escultor em barro com técnicas ancestrais"),
        ("Juliana Costa", "jucosta", "juliana.c@example.com", "555.666.777-88", "senha404", "ativo", "2023-06-12", "../app/static/assets/perfils/juliana.jpg", "Ilustradora digital com temas folclóricos"),
        ("Marcos Vinícius Rocha", "marcosvr", "marcos.rocha@example.com", "666.777.888-99", "senha505", "desativado", "2023-07-08", "../app/static/assets/perfils/marcos.jpg", "Artista têxtil com técnicas de bordado inovadoras"),
        ("Patrícia Mendes", "patymendes", "patricia.m@example.com", "777.888.999-00", "senha606", "ativo", "2023-08-25", "../app/static/assets/perfils/patricia.jpg", "Criadora de bijuterias artesanais com materiais naturais"),
        ("Lucas Gabriel Soares", "lucasgsoares", "lucas.g@example.com", "888.999.000-11", "senha707", "ativo", "2023-09-17", "../app/static/assets/perfils/lucas.jpg", "Especialista em cordel e literatura de cordel"),
        ("Isabela Martins", "isamartins", "isabela.m@example.com", "999.000.111-22", "senha808", "ativo", "2023-10-05", "../app/static/assets/perfils/isabela.jpg", "Artista de arte reciclada com consciência ambiental"),
        ("Roberto Ferreira", "robertofer", "roberto.f@example.com", "000.111.222-33", "senha909", "ativo", "2023-11-30", "../app/static/assets/perfils/roberto.jpg", "Pintor naïf com reconhecimento internacional"),
        ("Tatiane Ribeiro", "tatiribeiro", "tatiane.r@example.com", "123.987.456-00", "senha010", "ativo", "2023-12-12", "../app/static/assets/perfils/tatiane.jpg", "Artesã especializada em bonecas de pano regionais"),
        ("Antônio Carlos Jobim", "jobimarte", "jobim.art@example.com", "456.789.012-34", "senha111", "ativo", "2024-01-18", "../app/static/assets/perfils/jobim.jpg", "Escultor em madeira com influências indígenas"),
        ("Helena Souza", "helenas", "helena.s@example.com", "567.890.123-45", "senha121", "bloqueado", "2024-02-22", "../app/static/assets/perfils/helena.jpg", "Pintora abstrata com elementos da cultura popular"),
        ("Felipe Augusto", "felipeaug", "felipe.a@example.com", "678.901.234-56", "senha131", "ativo", "2024-03-07", "../app/static/assets/perfils/felipe.jpg", "Artista digital que mistura técnicas tradicionais"),
        ("Camila Ventura", "camilaventura", "camila.v@example.com", "789.012.345-67", "senha141", "ativo", "2024-04-14", "../app/static/assets/perfils/camila.jpg", "Ceramista utilitária com designs contemporâneos")
    ]
    
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    
    cursor.execute("""
        CREATE TEMPORARY TABLE temp_artistas (
            nome_completo VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            cpf_cnpj VARCHAR(18) NOT NULL,
            senha VARCHAR(100) NOT NULL,
            status_artista VARCHAR(15),
            data_cadastro DATETIME NOT NULL,
            url_avatar VARCHAR(100),
            biografia VARCHAR(200)
        )
    """)
    
    cursor.executemany("""
        INSERT INTO temp_artistas 
        (nome_completo, usuario, email, cpf_cnpj, senha, status_artista, data_cadastro, url_avatar, biografia) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, artistas)
    
    cursor.execute("""
        INSERT OR IGNORE INTO artistas 
        (nome_completo, usuario, email, cpf_cnpj, senha, status_artista, data_cadastro, url_avatar, biografia)
        SELECT nome_completo, usuario, email, cpf_cnpj, senha, status_artista, data_cadastro, url_avatar, biografia
        FROM temp_artistas
        WHERE NOT EXISTS (
            SELECT 1
            FROM artistas
            WHERE 
                usuario = temp_artistas.usuario OR
                email = temp_artistas.email OR
                cpf_cnpj = temp_artistas.cpf_cnpj
        )
    """)
    
    cursor.execute("DROP TABLE temp_artistas")
    
    con.commit()
    con.close()

def inserir_clientes():
    clientes = [
        ("Laura Mendonça", "lauramendonca", "laura.m@example.com", "111.222.333-44", "senha123", "ativo", "2023-01-05", "../app/static/assets/perfils/laura.jpg"),
        ("Pedro Henrique Alves", "pedroalves", "pedro.a@example.com", "222.333.444-55", "senha456", "ativo", "2023-01-10", "../app/static/assets/perfils/pedro.jpg"),
        ("Mariana Costa Silva", "marianacs", "mariana.cs@example.com", "333.444.555-66", "senha789", "ativo", "2023-02-15", "../app/static/assets/perfils/mariana.jpg"),
        ("Rafael Pereira", "rafaelp", "rafael.p@example.com", "444.555.666-77", "senha101", "bloqueado", "2023-03-08", "../app/static/assets/perfils/rafael.jpg"),
        ("Beatriz Oliveira", "biaoliveira", "beatriz.o@example.com", "555.666.777-88", "senha202", "ativo", "2023-04-20", "../app/static/assets/perfils/beatriz.jpg"),
        ("Lucas Martins", "lucasm", "lucas.m@example.com", "666.777.888-99", "senha303", "ativo", "2023-05-12", "../app/static/assets/perfils/lucas.jpg"),
        ("Isabela Santos", "isabelas", "isabela.s@example.com", "777.888.999-00", "senha404", "desativado", "2023-06-25", "../app/static/assets/perfils/isabela.jpg"),
        ("Gustavo Lima", "gustavol", "gustavo.l@example.com", "888.999.000-11", "senha505", "ativo", "2023-07-18", "../app/static/assets/perfils/gustavo.jpg"),
        ("Camila Rocha", "camilar", "camila.r@example.com", "999.000.111-22", "senha606", "ativo", "2023-08-30", "../app/static/assets/perfils/camila.jpg"),
        ("Bruno Carvalho", "brunoc", "bruno.c@example.com", "000.111.222-33", "senha707", "ativo", "2023-09-22", "../app/static/assets/perfils/bruno.jpg")
    ]
    
    con = sqlite3.connect("moiddo_arts.db")
    cursor = con.cursor()
    
    cursor.execute("""
        CREATE TEMPORARY TABLE temp_clientes (
            nome_completo VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            cpf VARCHAR(18) NOT NULL,
            senha VARCHAR(100) NOT NULL,
            status_cliente VARCHAR(15),
            data_cadastro DATETIME NOT NULL,
            url_avatar VARCHAR(100)
        )
    """)
    
    cursor.executemany("""
        INSERT INTO temp_clientes 
        (nome_completo, usuario, email, cpf, senha, status_cliente, data_cadastro, url_avatar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, clientes)
    
    cursor.execute("""
        INSERT OR IGNORE INTO cliente 
        (nome_completo, usuario, email, cpf, senha, status_cliente, data_cadastro, url_avatar)
        SELECT nome_completo, usuario, email, cpf, senha, status_cliente, data_cadastro, url_avatar
        FROM temp_clientes
        WHERE NOT EXISTS (
            SELECT 1
            FROM cliente
            WHERE 
                usuario = temp_clientes.usuario OR
                email = temp_clientes.email OR
                cpf = temp_clientes.cpf
        )
    """)
    
    cursor.execute("DROP TABLE temp_clientes")
    
    con.commit()
    con.close()

# Criar todas as tabelas
tabela_artistas()
tabela_cliente()
tabela_categorias()
tabela_obras()
tabela_carrinho()
tabela_item_carrinho()
tabela_pedido()
tabela_item_pedido()

# Popular as tabelas
inserir_categorias()
inserir_artistas()
inserir_clientes()