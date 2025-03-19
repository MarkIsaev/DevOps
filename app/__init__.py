from flask import Flask
from flask_login import LoginManager
from .extensions import db
from app.config import Config  # Путь к конфигурации
from sqlalchemy import inspect
from app.models import User, Category  # Импортируем модели User и Category
from app.admin import init_admin

def create_app():
    # Создаем приложение
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализация расширений
    db.init_app(app)
    
    # Инициализация login_manager
    login_manager = LoginManager()
    login_manager.login_view = 'login'  # Укажите страницу для перенаправления при неавторизованном доступе
    login_manager.init_app(app)  # Инициализация с Flask приложением

    # Инициализация админ-панели
    init_admin(app)
    
    # Использование before_request как альтернативы before_first_request
    @app.before_request
    def create_tables():
        """Создание таблиц, если их нет"""
        # Проверяем, существует ли таблица в базе данных
        if not inspect(db.engine).has_table('user'):  # Проверка существования таблицы 'user'
            db.create_all()

            # Добавление категорий
            if not Category.query.first():  # Если нет категорий в базе данных, добавим их
                categories = ['Work', 'Personal', 'Study', 'Hobby']
                for category_name in categories:
                    category = Category(name=category_name)
                    db.session.add(category)
                db.session.commit()

    # Импортируем роуты после инициализации приложения
    from .routes import init_routes
    init_routes(app, login_manager)

    return app