import unittest
from app import app, db
from models import User, Note
from flask import Flask

class NotesAppTests(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_and_login(self):
        # Регистрация нового пользователя
        response = self.app.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)

        # Логин с правильными данными
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект

        # Попытка логина с неправильным паролем
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertIn(b'Invalid credentials', response.data)  # Проверяем наличие сообщения об ошибке

    def test_create_note(self):
        # Логин
        self.app.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.app.post('/login', data={'username': 'testuser', 'password': 'password'})

        # Создание новой заметки
        response = self.app.post('/create_note', data={'title': 'Test Note', 'content': 'Test content'})
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект

        # Проверка, что заметка была добавлена
        note = Note.query.filter_by(title='Test Note').first()
        self.assertIsNotNone(note)
        self.assertEqual(note.content, 'Test content')

    def test_dashboard(self):
        # Логин
        self.app.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.app.post('/login', data={'username': 'testuser', 'password': 'password'})

        # Создание новой заметки
        self.app.post('/create_note', data={'title': 'Test Note', 'content': 'Test content'})

        # Получение страницы dashboard
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Note', response.data)  # Проверка, что заголовок заметки отображается на странице

    def test_logout(self):
        # Логин
        self.app.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.app.post('/login', data={'username': 'testuser', 'password': 'password'})

        # Логин с правильными данными
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект на главную страницу

        # Проверяем, что текущий пользователь больше не авторизован
        response = self.app.get('/dashboard')
        self.assertIn(b'Login', response.data)  # Проверяем, что кнопка логина снова доступна
