from flask import Blueprint,render_template, request, redirect,  url_for
import sqlite3

obras_bp = Blueprint('obras', __name__)


def get_db_connection():
    conn = sqlite3.connect('moiddo_arts.db')
    conn.row_factory = sqlite3.Row  
    return conn



@obras_bp.route('/loja', methods=['GET','POST'])
def filtrar_categorias():
    if request.method == 'GET':
        filtro = request.args.getlist('obras')
        selecionados = []

        if filtro:
            conn = get_db_connection()
            cursor = conn.cursor()

            placeholders = ','.join(['?' for _ in filtro])
            query = f"SELECT titulo,descricao,tecnica,dimensoes,preco,url_foto,status_obras,ano_criacao,data_cadastro FROM obras WHERE categoria IN ({placeholders})"

            cursor.execute(query, filtro)
            selecionados = cursor.fetchall()
            conn.close()

        else:
            mensagem = "Você não selecionou nenhuma fruta."
            conn = get_db_connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM obras")
            selecionados = cursor.fetchall()
            conn.close()

        # Passa as categorias para o template
        return render_template('/loja.html', obras=selecionados, user='user.avatar')
    #return redirect(url_for('obras.filtrar_categorias'))


