from .connection import db
from .seeders import popular_tabelas_inciais


def init_db():
    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS artistas(
            id_artista INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            cpf_cnpj VARCHAR(18) UNIQUE NOT NULL,
            senha VARCHAR(100) NOT NULL,
            status_artista VARCHAR(15) DEFAULT 'ativo' CHECK (status_artista IN ('ativo','desativado','bloqueado','inativo')),
            data_cadastro DATETIME NOT NULL,
            url_avatar VARCHAR(100),
            biografia VARCHAR(300),
            especialidade VARCHAR(200),
            tecnicasMateriais VARCHAR(300)
    )
"""         
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS cliente(
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            telefone VARCHAR(16) NOT NULL,
            cpf VARCHAR(18) UNIQUE NOT NULL,
            senha VARCHAR(100) NOT NULL,
            status_cliente VARCHAR(15) DEFAULT 'ativo' CHECK (status_cliente IN ('ativo','desativado','bloqueado','inativo')),
            data_cadastro DATETIME NOT NULL,
            url_avatar VARCHAR(100)
    )
"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS categoria(
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_categoria VARCHAR(100) NOT NULL,
            slug VARCHAR(50) UNIQUE NOT NULL
    )
"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS obras(
            id_obra INTEGER PRIMARY KEY AUTOINCREMENT,
            artista_id INTEGER,
            titulo VARCHAR(100) NOT NULL,
            descricao VARCHAR(200) NOT NULL,
            tecnica VARCHAR(100),
            dimensoes VARCHAR(100),
            preco DECIMAL(5,2) NOT NULL,
            categoria_id INTEGER NOT NULL,
            url_foto VARCHAR(100),
            status_obras VARCHAR(15) CHECK (status_obras IN ('ativa','rascunho','bloqueada','inativa')),
            estoque INTEGER NOT NULL,
            ano_criacao INTEGER,
            data_cadastro DATETIME,
            FOREIGN KEY(artista_id) REFERENCES artistas(id_artista),
            FOREIGN KEY(categoria_id) REFERENCES categoria(id_categoria)
            )
""" 
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS enderecos(
            id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            apelido VARCHAR(50) NOT NULL,
            rua VARCHAR(50) NOT NULL,
            cep VARCHAR(9) NOT NULL,
            logradouro VARCHAR(100) NOT NULL,
            numero VARCHAR(10) NOT NULL,
            complemento VARCHAR(50),
            bairro VARCHAR(50) NOT NULL,
            cidade VARCHAR(50) NOT NULL,
            estado VARCHAR(2) NOT NULL,
            principal BOOLEAN DEFAULT FALSE,
            FOREIGN KEY(cliente_id) REFERENCES cliente(id_cliente)
    )
"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS carrinho (
            id_carrinho INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            data_criacao DATETIME,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente)
)

"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS ItemCarrinho(
            id_itemCarrinho INTEGER PRIMARY KEY AUTOINCREMENT,
            carrinho_id INTEGER,
            obra_id INTEGER,
            quantidade INTEGER,
            FOREIGN KEY(carrinho_id) REFERENCES carrinho(id_carrinho),
            FOREIGN KEY(obra_id) REFERENCES obras(id_obra)
    )
"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS pedido(
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            status_pedido VARCHAR(15) DEFAULT 'pendente' CHECK (status_pedido IN ('pendente','finalizado','cancelado', 'entregue')),
            total_pedido DECIMAL(5,2) NOT NULL,
            data_criacao DATETIME NOT NULL,
            FOREIGN KEY(cliente_id) REFERENCES cliente(id_cliente)
    )
"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS ItemPedido(
            id_itemPedido INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER,
            obra_id INTEGER,
            preco_unitario DECIMAL(5,2) NOT NULL,
            quantidade INTEGER,
            FOREIGN KEY(pedido_id) REFERENCES pedido(id_pedido),
            FOREIGN KEY(obra_id) REFERENCES obras(id_obra)
)
"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS visualizacoes(
            id_visualizacao INTEGER PRIMARY KEY AUTOINCREMENT,
            artista_id INTEGER,
            obra_id INTEGER,
            id_visitante INTEGER,
            tipo_user VARCHAR(8) CHECK (tipo_user IN ('artista','cliente')),
            ip_visitante VARCHAR(45),
            data_visualizacao DATETIME NOT NULL,
            FOREIGN KEY (artista_id) REFERENCES artistas(id_artista),
            FOREIGN KEY(obra_id) REFERENCES obras(id_obra)
)
"""
        )
        cursor.execute(
            """CREATE TRIGGER IF NOT EXISTS verifica_limite_enderecos
            BEFORE INSERT ON enderecos
            FOR EACH ROW
            BEGIN
                SELECT CASE
                    WHEN (SELECT COUNT(*) FROM enderecos WHERE cliente_id = NEW.cliente_id) >= 6
                    THEN RAISE(ABORT, 'Limite de 6 endereços por cliente atingido')
                END;
            END;
"""
        )
        conn.commit()
        popular_tabelas_inciais()
