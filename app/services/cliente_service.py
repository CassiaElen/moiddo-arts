from ..database.models.model_cliente import Cliente

class ClienteService:
    def __init__(self, id_cliente=None):
        self.cliente = Cliente(id_cliente=id_cliente)
        if id_cliente:
            self.cliente.buscar_cliente_service()

    def salvar(self, campos):
        from datetime import datetime
        data_cadastro = datetime.now().strftime("%Y-%m-%d")
        self.cliente.nome_completo = campos["nome_completo"]
        self.cliente.usuario = campos["usuario"]
        self.cliente.email = campos["email"]
        self.cliente.telefone = campos["telefone"]
        self.cliente.cpf = campos["cpf"]
        self.cliente.senha = campos["senha"]
        self.cliente.data_cadastro = data_cadastro
        self.cliente.salvar()

    def editar(self, campos, imagem):
        self.cliente.nome_completo = campos["nome_completo"]
        self.cliente.usuario = campos["usuario"]
        self.cliente.telefone = campos["telefone"]
        self.cliente.email = campos["email"]
        self.cliente.cpf = campos["cpf"]

        if imagem:
            self.cliente.url_avatar = imagem

        self.cliente.salvar()
        
    def CheckLoginClient(self, email, senha):
        return self.cliente.CheckLoginClient(email, senha)
    
    def alterar_senha(self, senha_atual, nova_senha):
        if len(nova_senha) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not any(char.isdigit() for char in nova_senha):
            raise ValueError("A senha deve conter pelo menos 1 número")
        if not any(char in '!@#$%^&*()_+' for char in nova_senha):
            raise ValueError("A senha deve conter pelo menos 1 caractere especial")
        
        if self.cliente.senha != senha_atual:
            raise ValueError("Senha atual incorreta!")
        
        self.cliente.senha = nova_senha
        self.cliente.editar_senha()

        return "Senha alterada com sucesso!"
    
    def buscar_cliente(self):
        return self.cliente.buscar_cliente()
    
    def buscar_pedidos_filtrados(self, status, pagina, por_pagina):
        return self.cliente.buscar_pedidos_filtrados(status=status, pagina=pagina, por_pagina=por_pagina)