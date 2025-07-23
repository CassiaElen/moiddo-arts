from .categoria_seeder import seed_categorias
from .artistas_seeder import seed_artistas
from .cliente_seeder import seed_cliente
from .obras_seeder import seed_obras
from .enderecos_seeder import seed_enderecos
from .carrinho_seeder import seed_carrinho
from .item_carrinho_seeder import seed_item_carrinho
from .pedido_seeder import seed_pedido
from .item_pedido_seeder import seed_item_pedido

def popular_tabelas_inciais():
    seed_artistas()
    seed_categorias()
    seed_cliente()
    seed_obras()
    seed_enderecos()
    seed_carrinho()
    seed_item_carrinho()
    seed_pedido()
    seed_item_pedido()