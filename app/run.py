from app import create_app
import sqlite3

app = create_app()

if __name__ == "__main__":
    # Executar apenas uma vez para criar o banco
    from models import tabela_artistas, tabela_compradores, tabela_categorias, tabela_obras, tabela_carrinho, tabela_item_carrinho, tabela_pedido, tabela_item_pedido, inserir_categorias
    
    try:
        tabela_artistas()
        tabela_compradores()
        tabela_categorias()
        tabela_obras()
        tabela_carrinho()
        tabela_item_carrinho()
        tabela_pedido()
        tabela_item_pedido()
        inserir_categorias()
        print("✅ Banco de dados criado com sucesso!")
    except sqlite3.OperationalError:
        print("Tabelas já existentes")
    
    # Iniciar servidor
    app.run(debug=True, port=5152)