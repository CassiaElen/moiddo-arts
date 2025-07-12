from flask import render_template, request, redirect, url_for, flash, Blueprint
import sqlite3
from datetime import datetime
from ..services.authmanager import auth_manager

main = Blueprint('main', __name__)

#Função para cadastrar cliente:
def RegisterClient(nome_completo,usuario,email,cpf,senha): 
    conn = sqlite3.connect("moiddo_arts.db")
    cursor = conn.cursor()

    try:
        data_cadastro = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO cliente (nome_completo,usuario,email,cpf,senha,data_cadastro) VALUES (?,?,?,?,?,?)", (nome_completo,usuario,email,cpf,senha,data_cadastro))
        conn.commit()
    
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Se o Usuário já existir

    conn.close()
    return True

#Função para cadastrar Artista:
def RegisterArtist(nome_completo,usuario,email,cpf_cnpj,senha): # Adicionar o nome de usuário
    conn = sqlite3.connect("moiddo_arts.db")
    cursor = conn.cursor()

    try:
        data_cadastro = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO artistas (nome_completo,usuario,email,cpf_cnpj,senha, data_cadastro) VALUES (?,?,?,?,?,?)", (nome_completo,usuario,email,cpf_cnpj,senha, data_cadastro))
        conn.commit()
    
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Se o Usuário já existir

    conn.close()
    return True

# Função para verificar login do artista:
def CheckLoginArtist(email,senha):
    conn = sqlite3.connect("moiddo_arts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id_artista, email, senha, status_artista, url_avatar FROM artistas WHERE email=? AND senha=?",(email,senha))
    usuario_artista = cursor.fetchone()
    conn.close()
    return usuario_artista

#Função para verificar login do cliente:
def CheckLoginClient(email,senha):
    conn = sqlite3.connect("moiddo_arts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id_cliente, email, senha, status_cliente, url_avatar FROM cliente WHERE email=? AND senha=?",(email,senha))
    usuario_cliente = cursor.fetchone()
    conn.close()
    return usuario_cliente

#Rota inicial:
@main.route("/")
def PreLogin():
    return render_template("pre-login.html")

@main.route("/home")
def home():
    from ..services.artista_service import ArtistaService
    artista = ArtistaService()

    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","error")
        return redirect(url_for("main.PreLogin"))
    
    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()
    artistas = artista.buscar_artistasHome()
    return render_template("index.html",user=user, user_type=user_type, artistas=artistas)

@main.route("/sobre-nós")
def sobre_nos():
    return render_template("sobre-nós.html")

@main.route("/contatos")
def contato():
    return render_template("contato.html")

@main.route("/exposições")
def exposicoes():
    return render_template("exposicoes.html")

@main.route("/loja")
def loja():
    return render_template("loja.html")

@main.route("/artistas.comunidade")
def artistas():
    return render_template("artistas.comunidade.html")

@main.route("/carrinho")
def carrinho():
    return render_template("carrinho.html")

@main.route("/perfil-cliente")
def perfil_cliente():
    return render_template("perfil-cliente.html")

@main.route("/trocar-senha")
def trocar_senha():
    return render_template("trocar-senha.html")

@main.route("/politica-de-privacidade")
def politica_privacidade():
    return render_template("politica-privacidade.html")

@main.route("/termos-de-servico")
def termos_servico():
    return render_template("termos-servico.html")

@main.route("/deletar-conta")
def animacao_deletar_conta():
    return render_template("deletar-conta.html")

@main.route("/desativar-conta")
def animacao_desativar_conta():
    return render_template("desativar-conta.html")

@main.route("/login/cliente", methods=["GET","POST"])
def login_client():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        if not email or not senha:
            flash("Todos os campos são obrigatórios!","error")
            return(redirect(url_for("main.login_client")))
        
        user = CheckLoginClient(email, senha)
        if user:
            auth_manager.login_user('cliente', user)
            flash("Login realizado com sucesso!","success")
            return redirect(url_for("main.home"))
        else:
            flash("Email ou senha incorretos!", "error")
            return redirect(url_for("main.login_client"))
    return render_template("login-cliente.html")

@main.route("/login/artista", methods=["GET","POST"])
def login_artist():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        if not email or not senha:
            flash("Todos os campos são obrigatórios!","error")
            return redirect(url_for("main.login_artist"))
        
        user = CheckLoginArtist(email, senha)
        if user:
            auth_manager.login_user('artista',user)
            flash("Login realizado com sucesso!","success")
            return redirect(url_for("main.home"))
        else:
            flash("Email ou senha incorretos!","error")
            return redirect(url_for("main.login_artist"))
    return render_template("login-artista.html")

@main.route("/logout")
def logout():
    auth_manager.logout_user()
    flash("Logout realizado com sucesso!","success")
    return redirect(url_for("main.PreLogin"))

@main.route('/register/cliente', methods=['GET', 'POST'])
def register_client():
    if request.method == "POST":
        nome_completo = request.form["name"]
        usuario = request.form["user"]
        email = request.form["email"]
        cpf = request.form["cpf"]         
        senha = request.form["password"]

        if not email or not nome_completo or not senha or not cpf or not usuario:
            flash("Todos os campos são obrigatórios!","error")
            return redirect(url_for("main.register_client"))
        
        if RegisterClient(nome_completo,usuario,email,cpf,senha): 
            flash("Cadastro realizado com sucesso!","success")
            flash("Faça o seu login como Cliente!","success")
            return redirect(url_for("main.login_client"))
        else:
            flash("Usuário já cadastrado!","error")
            return redirect(url_for("main.register_client"))
    return render_template("cadastro-cliente.html")

@main.route("/register/artista", methods=["GET","POST"])
def register_artist():
    if request.method == "POST":
        nome_completo = request.form["name"]
        usuario = request.form["user"]
        email = request.form["email"]
        cpf_cnpj = request.form["cpf"]
        senha = request.form["password"]

        if not email or not nome_completo or not senha or not cpf_cnpj or not usuario: 
            flash("Todos os campos são obrigatórios!","error")
            return redirect(url_for("main.register_artist"))
        
        if RegisterArtist(nome_completo,usuario,email,cpf_cnpj,senha):
            flash("Cadastro realizado com sucesso!","success")
            flash("Faça o seu login como Artesão!","success")
            return redirect(url_for("main.login_artist"))
        else:
            flash("Usuário já cadastrado!","error")
            return redirect(url_for("main.register_artist"))
        
    return render_template("cadastro-artista.html")