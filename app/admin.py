from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField
from flask_login import current_user
from werkzeug.security import generate_password_hash
from .models import db, User, Note, Category

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['ADMIN_ENABLED'] = False  # Отключаем админку в тестах
    
    db.init_app(app)
    
    if app.config['ADMIN_ENABLED']:
        init_admin(app)
    
    return app

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

class AdminUserView(AdminModelView):
    column_exclude_list = ['password']
    form_extra_fields = {'password': PasswordField('Password')}

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data)

# Singleton pattern для админки
_admin_instance = None

def get_admin():
    global _admin_instance
    if _admin_instance is None:
        _admin_instance = Admin(name='Notes Admin', template_mode='bootstrap3')
    return _admin_instance

def init_admin(app):
    admin = get_admin()

    if not hasattr(app, 'admin_initialized'):
        admin.init_app(app)

        # Регистрация представлений с уникальными endpoint
        if not any(view.endpoint == 'admin_users_view' for view in admin._views):
            admin.add_view(AdminUserView(
                User, db.session,
                name='Users',
                endpoint='admin_users_view'
            ))
        
        if not any(view.endpoint == 'admin_notes_view' for view in admin._views):
            admin.add_view(ModelView(
                Note, db.session,
                name='Notes',
                endpoint='admin_notes_view'
            ))

        if not any(view.endpoint == 'admin_categories_view' for view in admin._views):
            admin.add_view(ModelView(
                Category, db.session,
                name='Categories',
                endpoint='admin_categories_view'
            ))

        app.admin_initialized = True


