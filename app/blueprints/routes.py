from flask import render_template, request, redirect, url_for, flash, Blueprint
from ..services.authmanager import auth_manager
from ..services.validacoes_service import (
    validar_campos,
    regras_registrar_perfil_cliente,
    regras_registrar_perfil_artista
)

main = Blueprint('main', __name__)

#Rota inicial:
@main.route("/")
def PreLogin():
    return render_template("pre-login.html")

@main.route("/home")
def home():
    from ..services.artista_service import ArtistaService
    from ..services.obras_service import Obras
    artista = ArtistaService()
    obra = Obras()

    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()
    artistas = artista.buscar_artistasHome()
    obras_destaque = obra.buscar_obrasHome()
    return render_template("index.html",user=user, user_type=user_type, artistas=artistas, obras_destaque=obras_destaque)

@main.route("/sobre-nos")
def sobre_nos():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()
    return render_template("sobre-nos.html",user=user, user_type=user_type)

@main.route("/contato")
def contato():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()
    return render_template("contato.html",user=user, user_type=user_type)

@main.route("/loja")
def loja():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()
    return render_template("loja.html",user=user, user_type=user_type)

@main.route("/carrinho")
def carrinho():
    if not auth_manager.is_client():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))

    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()
    return render_template("carrinho.html",user=user, user_type=user_type)

@main.route("/politica-de-privacidade")
def politica_privacidade():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    return render_template("politica-privacidade.html")

@main.route("/termos-de-servico")
def termos_servico():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    return render_template("termos-servico.html")

@main.route("/deletar-conta")
def animacao_deletar_conta():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    return render_template("deletar-conta.html")

@main.route("/desativar-conta")
def animacao_desativar_conta():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    return render_template("desativar-conta.html")

@main.route("/perfil-cliente")
def perfil_cliente():
    if not auth_manager.is_client():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))

    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()
    return render_template("perfil-cliente.html",user=user, user_type=user_type)

@main.route("/trocar-senha", methods=["GET", "POST"]) 
def trocar_senha():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.", "alert-error")
        return redirect(url_for("main.PreLogin"))
    
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not all([current_password, new_password, confirm_password]):
            flash("Todos os campos são obrigatórios.", "alert-error")
            return redirect(url_for("main.trocar_senha"))
        
        user_type = auth_manager.current_user_type()

        try:
            if user_type == "artista":
                from ..services.artista_service import ArtistaService
                service = ArtistaService(id_artista=auth_manager.get_current_user_id())
            else:
                from ..services.cliente_service import ClienteService
                service = ClienteService(id_cliente=auth_manager.get_current_user_id())

            result = service.alterar_senha(current_password, new_password)
            if result:
                flash(result, "alert-success")
            return redirect(url_for("main.PreLogin"))
        except Exception as e:
            flash(str(e), "alert-error")
    return render_template("trocar-senha.html")

@main.route("/login/cliente", methods=["GET","POST"])
def login_client():
    from ..services.cliente_service import ClienteService
    service_cliente = ClienteService()

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        if not all([email, senha]):
            flash("Todos os campos são obrigatórios!","alert-error")
            return(redirect(url_for("main.login_client")))

        user = service_cliente.CheckLoginClient(email, senha)
        if user:
            from ..services.tratarLogin_service import handle_artist_login
            return handle_artist_login(user, "cliente", "main.login_client" )
        else:
            flash("Email ou senha incorretos!", "alert-error")
            return redirect(url_for("main.login_client"))
    return render_template("login-cliente.html")

@main.route("/login/artista", methods=["GET","POST"])
def login_artist():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        if not all([email, senha]):
            flash("Todos os campos são obrigatórios!","alert-error")
            return redirect(url_for("main.login_artist"))
        
        from ..services.artista_service import ArtistaService
        service = ArtistaService()
        user = service.CheckLoginArtist(email, senha)

        if not user:
            flash("Email ou senha incorretos!", "alert-error")
            return redirect(url_for("main.login_artist"))
        
        from ..services.tratarLogin_service import handle_artist_login
        return handle_artist_login(user, "artista", "main.login_artist")
    
    return render_template("login-artista.html")

@main.route("/logout")
def logout():
    auth_manager.logout_user()
    flash("Logout realizado com sucesso!","alert-success")
    return redirect(url_for("main.PreLogin"))

@main.route('/register/cliente', methods=['GET', 'POST'])
def register_client():
    from ..services.cliente_service import ClienteService
    service_cliente = ClienteService()
    if request.method == "POST":
        campos = {
            "nome_completo": request.form.get("name"),
            "usuario": request.form.get("user"),
            "email": request.form.get("email"),
            "cpf": request.form.get("cpf"),
            "senha": request.form.get("password")
        }
        
        erros = validar_campos(campos, regras_registrar_perfil_cliente())
        if erros:
            for erro in erros:
                flash(erro, "alert-error")
                return redirect(url_for("main.register_client"))
        service_cliente.salvar(campos)
        flash("Conta registrada com sucesso", "alert-success")
        return redirect(url_for("main.login_client"))
    return render_template("cadastro-cliente.html")

@main.route("/register/artista", methods=["GET","POST"])
def register_artist():
    from ..services.artista_service import ArtistaService
    service_artista = ArtistaService()
    if request.method == "POST":
        campos = {
            "nome_completo": request.form.get("name"),
            "usuario": request.form.get("user"),
            "email": request.form.get("email"),
            "cpf": request.form.get("cpf"),
            "senha": request.form.get("password")
        }
        erros = validar_campos(campos, regras_registrar_perfil_artista())
        if erros:
            for erro in erros:
                flash(erro, "alert-error")
                return redirect(url_for("main.register_artist"))
        
        service_artista.salvar(campos)
        flash("Conta registrada com sucesso", "alert-success")
        return redirect(url_for("main.login_artist"))
    return render_template("cadastro-artista.html")