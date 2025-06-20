from ..database.models.model_categoria import Categoria

class CategoriaService:

    def buscar_categorias(self):
        categoria = Categoria()
        return  categoria.buscar_todas_categoria()
service_categorias = CategoriaService()