from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
import sqlite3
import hashlib
from datetime import datetime

main = Blueprint('main', __name__)

#Função para cadastrar cliente:
def RegisterClient(email,nome_completo,senha,cpf,usuario): # Adicionar o nome de usuário e o cpf
    conn = sqlite3.connect("moiddo_arts.db")
    cursor = conn.cursor()

    try:
        data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO comprador (email,nome_completo,senha,cpf,usuario,data_cadastro) VALUES (?,?,?,?,?,?)", (email,nome_completo,senha,cpf,usuario,data_cadastro))
        conn.commit()
    
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Se o Usuário já existir

    conn.close()
    return True

#Função para cadastrar Artista:
def RegisterArtist(email, nome_completo, senha, cpf_cnpj,usuario): # Adicionar o nome de usuário
    conn = sqlite3.connect("moiddo_arts.db")
    cursor = conn.cursor()

    try:
        data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO artistas (email,nome_completo,senha,cpf_cnpj,usuario,data_cadastro) VALUES (?,?,?,?,?,?)", (email,nome_completo,senha,cpf_cnpj,usuario,data_cadastro))
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

    cursor.execute("SELECT * FROM artistas WHERE email=? AND senha=?",(email,senha))
    usuario_artista = cursor.fetchone()
    conn.close()
    return usuario_artista

#Função para verificar login do cliente:
def CheckLoginClient(email,senha):
    conn = sqlite3.connect("moiddo_arts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cliente WHERE email=? AND senha=?",(email,senha))
    usuario_cliente = cursor.fetchone()
    conn.close()
    return usuario_cliente

#Rota inicial:
@main.route("/")
def PreLogin():
    return render_template("Pré-login.html")

@main.route("/home")
def home():
    return render_template("index.html")


@main.route("/login/cliente", methods=["GET","POST"])
def login_client():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        if not email or not senha:
            flash("Todos os campos são obrigatórios!")
            return(redirect(url_for("login_client")))
        
        user = CheckLoginClient(email, senha)
        if user:
            flash("Login realizado com sucesso!")
            return redirect(url_for("home"))
        else:
            flash("Email ou senha incorretos!")
            return redirect(url_for("login_client"))
    return render_template("login-cliente.html")

@main.route("/login/artista", methods=["GET","POST"])
def login_artist():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        if not email or not senha:
            flash("Todos os campos são obrigatórios!")
            return redirect(url_for("login_artist"))
        
        user = CheckLoginArtist(email, senha)
        if user:
            flash("Login realizado com sucesso!")
            return redirect(url_for("home"))
        else:
            flash("Email ou senha incorretos!")
            return redirect(url_for("login_artist"))
    return render_template("login-artesao.html")


@main.route('/register/cliente', methods=['GET', 'POST'])
def register_client():
    if request.method == "POST":
        email = request.form.get("email")
        nome_completo = request.form.get("name")
        senha = request.form.get("password")
        cpf = request.form.get("cpf")  
        usuario = request.form.get("user")

        if not email or not nome_completo or not senha or not cpf or not usuario:
            flash("Todos os campos são obrigatórios!")
            return redirect(url_for("register_client"))
        
        if RegisterClient(email,nome_completo,senha,cpf,usuario): 
            flash("Cadastro realizado com sucesso!")
            flash("Faça o seu login como Cliente!")
            return redirect(url_for("login_client"))
        else:
            flash("Usuário já cadastrado!")
            return redirect(url_for("register_client"))
    return render_template("cadastro-cliente.html")

@main.route("/register/artista", methods=["GET","POST"])
def register_artist():
    if request.method == "POST":
        email = request.form["email"]
        nome_completo = request.form["name"]
        senha = request.form["password"]
        cpf_cnpj = request.form["cpf"]
        usuario = request.form["name"]

        if not email or not nome_completo or not senha or not cpf_cnpj or not usuario: 
            flash("Todos os campos são obrigatórios!")
            return redirect(url_for("register_artist"))
        
        if RegisterArtist(email, nome_completo, senha, cpf_cnpj,usuario):
            flash("Cadastro realizado com sucesso!")
            flash("Faça o seu login com Artesão!")
            return redirect(url_for("login_artist"))
        else:
            flash("Usuário já cadastrado!")
            return redirect(url_for("register_artist"))
        
    return render_template("cadastro-artesao.html")