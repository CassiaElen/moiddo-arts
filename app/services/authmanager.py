from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, session,get_flashed_messages
import sqlite3
import hashlib
from datetime import datetime, timedelta

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
        session['user'] = user_data
        session.modified = True

    def logout_user(self):
        session.pop('user', None)
        session.pop('user_type', None)

    def is_authenticated(self):
        return 'user' in session

    def current_user(self):
        return session.get('user')

# Instância do AuthManager (será associada à aplicação principal depois)
auth_manager = AuthManager()