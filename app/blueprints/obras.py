from flask import Blueprint,render_template, request, redirect,  url_for
import sqlite3

obras_bp = Blueprint('obras', __name__)


def get_db_connection():
    conn = sqlite3.connect('moiddo_arts.db')
    conn.row_factory = sqlite3.Row  
    return conn



@obras_bp.route('/loja', methods=['POST'])
def filtrar_categorias():
    if request.method == 'POST':
        filtro = request.form.getlist('obras')
        selecionados = []

        if filtro:
            conn = get_db_connection()
            cursor = conn.cursor()

            placeholders = ','.join(['?' for _ in filtro])
            query = f"SELECT titulo,descricao,tecnica,dimensoes,preco,url_foto,status_obras  FROM obras WHERE nome IN ({placeholders})"

            cursor.execute(query, filtro)
            selecionados = cursor.fetchall()
            conn.close()

        else:
            mensagem = "Você não selecionou nenhuma fruta."

        # Passa as categorias para o template
        return render_template('loja.html', obras=selecionados)
    return redirect(url_for('loja'))


