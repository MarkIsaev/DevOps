from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Note, Category, shared_notes

def init_routes(app, login_manager):
    # Инициализация загрузчика пользователя
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('home.html', categories=Category.query.all())

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])
            
            if User.query.filter((User.username == username) | (User.email == email)).first():
                flash('Username or email already exists', 'danger')
                return redirect(url_for('register'))
            
            db.session.add(User(username=username, email=email, password=password))
            db.session.commit()
            
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('notes'))
        
        if request.method == 'POST':
            user = User.query.filter_by(username=request.form['username']).first()
            
            if user and check_password_hash(user.password, request.form['password']):
                login_user(user)
                return redirect(url_for('notes'))
            else:
                flash('Invalid username or password.', 'danger')
        
        return render_template('login.html')

    @app.route("/logout", methods=["GET", "POST"])
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('home'))

    @app.route('/notes')
    @login_required
    def notes():
        user_notes = Note.query.filter_by(user_id=current_user.id).all()
        shared_notes = current_user.shared_notes

        return render_template(
            'notes.html', 
            user_notes=user_notes,
            shared_notes=shared_notes,
            categories=Category.query.all(),
            users=User.query.all()
        )

    @app.route('/add_note', methods=['GET', 'POST'])
    @login_required
    def add_note():
        if request.method == 'POST':
            category_id = request.form.get('category')
            if not category_id:
                flash('Category is required.', 'danger')
                return redirect(url_for('add_note'))
            
            note = Note(
                title=request.form['title'], 
                content=request.form['content'], 
                user_id=current_user.id, 
                category_id=category_id
            )
            db.session.add(note)
            db.session.commit()
            flash('Note added!', 'success')
            return redirect(url_for('notes'))
        
        return render_template('add_note.html', categories=Category.query.all())

    @app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
    @login_required
    def edit_note(note_id):
        note = Note.query.get_or_404(note_id)

        if note.user_id != current_user.id:
            flash('Not authorized!', 'danger')
            return redirect(url_for('notes'))
        
        if request.method == 'POST':
            note.title = request.form['title']
            note.content = request.form['content']
            note.category_id = request.form.get('category')
            db.session.commit()
            flash('Note updated!', 'success')
            return redirect(url_for('notes'))
        
        return render_template('edit_note.html', note=note, categories=Category.query.all())

    @app.route('/delete_note/<int:note_id>', methods=['POST'])
    @login_required
    def delete_note(note_id):
        note = Note.query.get_or_404(note_id)
        
        if note.user_id != current_user.id:
            flash('Not authorized!', 'danger')
            return redirect(url_for('notes'))
        
        db.session.query(shared_notes).filter_by(note_id=note.id).delete()
        db.session.commit()

        db.session.delete(note)
        db.session.commit()
        flash('Note deleted!', 'success')
        return redirect(url_for('notes'))

    @app.route('/share_note/<int:note_id>', methods=['GET', 'POST'])
    @login_required
    def share_note(note_id):
        note = Note.query.get_or_404(note_id)

        if request.method == 'POST':
            user = User.query.filter_by(username=request.form.get('username')).first()
            
            if user:
                note.shared_with_users.append(user)
                db.session.commit()
                flash(f'Note successfully shared with {user.username}', 'success')
            else:
                flash('User not found.', 'danger')

            return redirect(url_for('share_note', note_id=note_id))

        return render_template('share_note.html', note=note)

    @app.route('/admin')
    @login_required
    def admin_panel():
        if not current_user.is_admin():
            flash('Access denied! You are not an admin.', 'danger')
            return redirect(url_for('home'))

        users = User.query.all()
        notes = Note.query.all()
        
        return render_template('admin_panel.html', users=users, notes=notes)
