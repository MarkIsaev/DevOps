import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # База данных SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False