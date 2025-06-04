from app import create_app
import sqlite3

app = create_app()

def inicializar_banco():
    #Inicializa o banco criando primeiro as tabelas e segundo os inserts
    from app.models import (
        tabela_artistas, tabela_cliente, tabela_categorias, tabela_obras,
        tabela_carrinho, tabela_item_carrinho, tabela_pedido, tabela_item_pedido,
        inserir_categorias, inserir_artistas, inserir_clientes
    )

    # Ordem correta da criação de tabelas respeitando as chaves estrangeiras
    funcoes_criar = [
        tabela_artistas,
        tabela_cliente,
        tabela_categorias,
        tabela_obras,
        tabela_carrinho,
        tabela_item_carrinho,
        tabela_pedido,
        tabela_item_pedido
    ]
    # Define os dados a inserir
    funcoes_dados = [
        inserir_categorias,
        inserir_artistas,
        inserir_clientes
    ]

    try:
        for func in funcoes_criar:
            func()
        for func in funcoes_dados:
            func()

        print("Banco de dados inicializado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

if __name__ == "__main__":
    #inicializa o banco de dados
    inicializar_banco()

    # Iniciar servidor
    app.run(debug=True, port=5152)

    """ 
    # Executar apenas uma vez para criar o banco
    from app.models import tabela_artistas, tabela_cliente, tabela_categorias, tabela_obras, tabela_carrinho, tabela_item_carrinho, tabela_pedido, tabela_item_pedido, inserir_categorias, inserir_artistas, inserir_clientes
    
    try:
        tabela_artistas()
        tabela_cliente()
        tabela_categorias()
        tabela_obras()
        tabela_carrinho()
        tabela_item_carrinho()
        tabela_pedido()
        tabela_item_pedido()
        inserir_categorias()
        inserir_artistas()
        inserir_clientes()
        print("Banco de dados criado com sucesso!")
    except sqlite3.OperationalError:
        print("Tabelas já existentes")
    """