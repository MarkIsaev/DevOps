import unittest
from app import create_app, db
from app.models import User, Note, Category  # Добавили Category
from flask import Flask

class NotesAppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'ADMIN_ENABLED': False  # Отключаем админку в тестах
        })
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        # Регистрация
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Проверяем создание пользователя в БД
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)

        # Логин
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что на странице есть кнопка "Return to Notes", которая появляется только после логина
        self.assertIn(b'My Notes - Notes App', response.data)  # Теперь проверяем, что эта кнопка есть


    def test_create_note(self):
        # Регистрация
        self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        # Логин
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)

        # Создание категории через API
        self.client.post('/add_category', data={'name': 'Test Category'})
        
        # Создание заметки
        response = self.client.post('/add_note', data={
            'title': 'Test Note',
            'content': 'Content',
            'category': 1
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        note = Note.query.first()
        self.assertIsNotNone(note)

    def test_dashboard(self):
        # Регистрация и логин
        self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

        # Создаем категорию и заметку
        category = Category(name="Test Category")
        db.session.add(category)
        db.session.commit()
        
        self.client.post('/add_note', data={
            'title': 'Test Note',
            'content': 'Test content',
            'category': category.id
        })

        # Проверяем dashboard
        response = self.client.get('/notes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Note', response.data)

    def test_logout(self):
    # Регистрация и логин
        self.client.post('/register', data={
            'username': 'testuser',
            'password': 'password123',
            'email': 'test@example.com',
            'confirm_password': 'password123'
        })
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

        # Выход
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Проверка доступа к защищенной странице
        response = self.client.get('/notes', follow_redirects=True)
        self.assertNotIn(b'Test Note', response.data)

if __name__ == '__main__':
    unittest.main()