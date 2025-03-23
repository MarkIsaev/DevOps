from flask_login import UserMixin
from app.extensions import db
from datetime import datetime

# Явное объявление Base


shared_notes = db.Table('shared_notes',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # Добавлено поле для роли
    date_created = db.Column(db.DateTime, default=db.func.now())  # Дата регистрации

    # Добавление метода is_active
    def is_active(self):
        return True  # Метод должен возвращать True или False. В данном случае всегда возвращаем True
    
    # Связь с заметками, которые были поделены
    shared_notes = db.relationship('Note', secondary='shared_notes', backref=db.backref('shared_with_users', lazy='dynamic'))

    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

# Таблица для связи заметок с пользователями, с которыми они поделены

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('notes', lazy=True))
    category = db.relationship('Category', backref='notes', lazy=True)

    def __repr__(self):
        cat = self.category.name if self.category else "No Category"
        return f'<Note {self.title} - {cat}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('categories', lazy=True))

    def __repr__(self):
        return f'<Category {self.name}>'