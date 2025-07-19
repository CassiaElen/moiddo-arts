from flask import flash, redirect, url_for
from ..services.authmanager import auth_manager

def handle_artist_login(result, user_type, login):

    status = result.get('status')

    if not status:
        flash("Erro no sistema: status não encontrado", "alert-error")
        return redirect(url_for('main.PreLogin'))
    
    if status == 'ativo':
        auth_manager.login_user(user_type, result)
        flash('Login realizado com sucesso!', 'alert-success')
        return redirect(url_for('main.home'))
    
    elif status == 'desativado':
        auth_manager.login_user(user_type, result)
        flash('Reativamos sua conta, seja bem vindo de volta.', 'alert-success')
        return redirect(url_for('main.home'))
    
    elif status == 'bloqueado':
        flash('Sua conta foi bloqueada por violar as deretrizes da plataforma. Entre em contato com o suporte.\n suporte.muiddoartes@example.com', 'alert-error')
        return redirect(url_for('main.PreLogin'))
    
    elif status == 'inativo':
        flash("Email ou senha incorretos!", "alert-error")
        return redirect(url_for(login))
    
    else:
        flash('Status de conta desconhecido', 'alert-error')
        return redirect(url_for('main.PreLogin'))