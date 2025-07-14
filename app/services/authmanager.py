from flask import session
from datetime import timedelta

# Classe para gerenciar autenticação:
class AuthManager:
    def __init__(self, app=None):
        self.session_lifetime = timedelta(minutes=30)
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.session_lifetime = app.config.get('PERMANENT_SESSION_LIFETIME', timedelta(minutes=30))
        app.permanent_session_lifetime = self.session_lifetime

    def login_user(self, user_type, user_data):
        session.permanent = True
        session['user_type'] = user_type

        if isinstance(user_data, tuple):
            session['user'] = {
                'id':user_data[0],
                'email':user_data[1],
                'status':user_data[3],
                'avatar':user_data[4]
            }
        else:
            session['user'] = user_data

        session.modified = True

    def logout_user(self):
        session.pop('user', None)
        session.pop('user_type', None)

    def is_authenticated(self):
        return 'user' in session

    def current_user(self):
        return session.get('user')
    
    def current_user_type(self):
        return session.get('user_type')

    def get_current_user_id(self):
        user = session.get('user')
        return user['id'] if user else None

# Instância do AuthManager (será associada à aplicação principal depois)
auth_manager = AuthManager()