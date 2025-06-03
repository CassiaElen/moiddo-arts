from flask import Flask, render_template, request, redirect, send_from_directory, abort, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_migrate import Migrate
import uuid
import mimetypes

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' #UPLOAD_FOLDER
# impede que arquivos maiores do que 5MB sejam aceitos.
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 megabytes
# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nomes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#Configuração do LoginManager:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # Redireciona para a página de login caso o usuário não esteja autenticado

# Modelo de dados
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

# Modelo de Usuário
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

class Arquivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_original = db.Column(db.String(200))
    nome_armazenado = db.Column(db.String(200), unique=True)
    caminho = db.Column(db.String(300))
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    descricao = db.Column(db.Text, nullable=True)


# Criação das tabelas
with app.app_context():
    db.create_all()

# Função para checar se o arquivo é permitido:
def arquivo_permitido(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#tratar erro
@app.errorhandler(413)
def arquivo_grande_erro(e):
    return 'Arquivo muito grande. O limite é 5MB.', 413

def salvar_arquivo(arquivo):
    nome_original = secure_filename(arquivo.filename)
    extensao = nome_original.rsplit('.', 1)[-1].lower()

    # Detecta tipo de arquivo
    tipo_mime, _ = mimetypes.guess_type(nome_original)
    if tipo_mime:
        categoria = tipo_mime.split('/')[0]  # image, application, text, etc.
    else:
        categoria = 'outros'

    # Cria subpasta se necessário
    subpasta = os.path.join(app.config['UPLOAD_FOLDER'], categoria)
    os.makedirs(subpasta, exist_ok=True)

    nome_unico = f"{uuid.uuid4()}.{extensao}"
    caminho = os.path.join(subpasta, nome_unico)
    arquivo.save(caminho)

    return nome_original, nome_unico, caminho

# Define a rota principal
@app.route("/")
def home():
    return "Olá, Flask ☆*: .｡. o(≧▽≦)o .｡.:*☆"

@app.route("/sobre")
def sobre():
    return "Esta é a página sobre ヾ(＠⌒ー⌒＠)ノ"

@app.route("/contato")
def contato():
    return "Entre em contato conosco! （づ￣3￣）づ╭❤️～"

@app.route("/usuario/<nome>")
def saudacao(nome):
    return f"Olá!, {nome.capitalize()}! \(@^0^@)/ "

@app.route("/quadrado/<int:numero>")
def quadrado(numero):
    return f"O quadrado de {numero} é {numero ** 2}"

@app.route("/bemvindo/<nome>")
def bemvindo(nome):
    return render_template("index.html", nome=nome)

@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        nome_digitado = request.form.get("nome")
        nova_pessoa = Pessoa(nome=nome_digitado)
        db.session.add(nova_pessoa)
        db.session.commit()
        return redirect("/formulario")

    pessoas = Pessoa.query.all()
    return render_template("formulario.html", pessoas=pessoas)

@app.route("/deletar/<int:id>")
def deletar(id):
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect("/formulario")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    pessoa = Pessoa.query.get_or_404(id)

    if request.method == 'POST':
        novo_nome = request.form["nome"]
        pessoa.nome = novo_nome
        db.session.commit()
        return redirect("/formulario")
    
    return render_template("editar.html", pessoa = pessoa)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])
        
        if Usuario.query.filter_by(email=email).first():
            return "Usuário já existe!"
        
        novo = Usuario(email=email, senha=senha)
        db.session.add(novo)
        db.session.commit()
        return redirect("/login")
    
    return render_template("cadastro.html")

app.secret_key = 'segredo'  # Necessário para usar sessões

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)  # Faz o login com o Flask-Login
            return redirect("/painel")
        else:
            return "Login inválido" # não retorna pro login.html
    
    return render_template("login.html")

@app.route("/painel")
@login_required  # Só pode ser acessada se o usuário estiver logado
def painel():
    return f"Bem-vindo ao painel, {current_user.email}! <a href='/logout'>Sair</a>"

@app.route("/logout")
def logout():
    logout_user()  # Faz o logout com o Flask-Login
    return redirect("/login")

# Carregar usuário na sessão
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        arquivos = request.files.getlist('arquivo')
        descricao = request.form.get('descricao')

        if len(arquivos) > 1:
            return "Erro: esta rota só permite o envio de **um único arquivo**."

        arquivo = arquivos[0] if arquivos else None
        if not arquivo or arquivo.filename == '':
            return 'Arquivo inválido.'
        
        if 'arquivo' not in request.files:
            return 'Nenhum arquivo enviado.'
        
        if arquivo:
            nome_original, nome_unico, caminho = salvar_arquivo(arquivo)

            novo_arquivo = Arquivo(
                nome_original=nome_original,
                nome_armazenado=nome_unico,
                caminho=caminho,
                descricao=descricao
            )
            db.session.add(novo_arquivo)
            db.session.commit()

            return redirect(url_for('listar_arquivos'))

    return render_template('upload.html')

#acessar os arquivos com URLs como:
#http://localhost:5000/uploads/nome_do_arquivo.jpg
@app.route('/arquivos/<int:id>')
def arquivo_enviado(id):
    arquivo = Arquivo.query.get_or_404(id)
    return send_file(arquivo.caminho)

@app.route('/arquivos')
def listar_arquivos():
    tipo = request.args.get('tipo')
    page = request.args.get('page', 1, type=int)
    por_pagina = 10

    query = Arquivo.query
    if tipo:
        query = query.filter(Arquivo.nome_original.ilike(f'%.{tipo}'))

    arquivos_paginados = query.order_by(Arquivo.data_envio.desc()).paginate(page=page, per_page=por_pagina)

    for arq in arquivos_paginados.items:
        try:
            arq.tamanho_kb = os.path.getsize(arq.caminho) // 1024
        except:
            arq.tamanho_kb = 0

    return render_template('lista_arquivos.html', arquivos=arquivos_paginados.items, tipo=tipo, paginacao=arquivos_paginados)

@app.route('/delete/<nome_arquivo>', methods=['POST'])
def deletar_arquivo(nome_arquivo):
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
    if os.path.exists(caminho):
        os.remove(caminho)

    # Remover do banco
    registro = Arquivo.query.filter_by(nome_armazenado=nome_arquivo).first()
    if registro:
        db.session.delete(registro)
        db.session.commit()

    return redirect(url_for('listar_arquivos'))

@app.route('/upload-multiplos', methods=['GET', 'POST'])
def upload_multiplos():
    if request.method == 'POST':
        arquivos = request.files.getlist('arquivo')

        if not arquivos or arquivos == [None]:
            return 'Nenhum arquivo enviado.'

        for arquivo in arquivos:
            if not arquivo or arquivo.filename == '':
                continue  # pula arquivos inválidos

            nome_original, nome_unico, caminho = salvar_arquivo(arquivo)

            novo_arquivo = Arquivo(
                nome_original=nome_original,
                nome_armazenado=nome_unico,
                caminho=caminho
            )
            db.session.add(novo_arquivo)

        db.session.commit()
        return redirect(url_for('listar_arquivos'))

    return render_template('upload_multiplos.html')

@app.route('/abrir/<int:id>')
def abrir_arquivo(id):
    arquivo = Arquivo.query.get_or_404(id)
    if not os.path.exists(arquivo.caminho):
        return 'Arquivo não encontrado.', 404
    return send_file(arquivo.caminho, as_attachment=False)

@app.route('/editar_descricao/<int:id>', methods=['GET', 'POST'])
@login_required  # se estiver usando login
def editar_descricao(id):
    arquivo = Arquivo.query.get_or_404(id)

    if request.method == 'POST':
        nova_descricao = request.form.get('descricao')
        arquivo.descricao = nova_descricao
        db.session.commit()
        return redirect(url_for('listar_arquivos'))

    return render_template('editar_descricao.html', arquivo=arquivo)


@app.route('/editarseila/<int:id>', methods=['GET', 'POST'])
def editar_seila(id):
    arquivo = Arquivo.query.get_or_404(id)
    
    conteudo_txt = None
    if arquivo.caminho_arquivo.endswith('.txt'):
        try:
            caminho_absoluto = os.path.join(app.static_folder, arquivo.caminho_arquivo)
            with open(caminho_absoluto, 'r', encoding='utf-8') as f:
                conteudo_txt = f.read()
        except Exception as e:
            conteudo_txt = f"Erro ao ler o arquivo .txt: {str(e)}"

    if request.method == 'POST':
        nova_descricao = request.form.get('descricao')
        arquivo.descricao = nova_descricao
        db.session.commit()
        return redirect(url_for('listar_arquivos'))

    return render_template('editar_descricao.html', arquivo=arquivo, conteudo_txt=conteudo_txt)

# Executa o servidor se este arquivo for o principal
if __name__ == "__main__":
    app.run(debug=True) # ativa a atualização automatica quando o codigo muda(só usar em desenvolvimento)