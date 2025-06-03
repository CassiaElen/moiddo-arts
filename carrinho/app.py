from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave-secreta-muito-forte'

# ====== Função para conectar ao banco ======
def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# ====== Rota inicial: listar produtos ======
@app.route('/')
def index():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

# ====== Adicionar ao carrinho ======
@app.route('/adicionar/<int:produto_id>')
def adicionar(produto_id):
    carrinho = session.get('carrinho', [])
    if produto_id not in carrinho:
        carrinho.append(produto_id)
    session['carrinho'] = carrinho
    return redirect('/')

# ====== Ver carrinho ======
@app.route('/carrinho')
def carrinho():
    carrinho_ids = session.get('carrinho', [])
    if not carrinho_ids:
        return render_template('carrinho.html', produtos=[])

    placeholders = ','.join('?' for _ in carrinho_ids)
    conn = get_db_connection()
    query = f'SELECT * FROM produtos WHERE id IN ({placeholders})'
    produtos = conn.execute(query, carrinho_ids).fetchall()
    conn.close()
    return render_template('carrinho.html', produtos=produtos)

# ====== Limpar carrinho ======
@app.route('/limpar')
def limpar():
    session.pop('carrinho', None)
    return redirect('/carrinho')

if __name__ == '__main__':
    app.run(debug=True)
