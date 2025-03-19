from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms.fields import PasswordField
from werkzeug.security import generate_password_hash
from .models import db, User, Note, Category

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

class AdminUserView(AdminModelView):
    column_exclude_list = ['password']
    
    # Ensure form_extra_fields is correctly defined as a dictionary
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data)

# Admin initialization
admin = Admin(name='Admin Panel', template_mode='bootstrap3', endpoint='admin_panel')

def init_admin(app):
    # Only initialize if not already done
    if getattr(app, 'admin_initialized', False):
        return
    
    admin.init_app(app)
    admin.add_view(AdminUserView(User, db.session, endpoint='admin_user_view', name='Admin Users'))
    admin.add_view(AdminModelView(Note, db.session, endpoint='admin_note_view', name='Admin Notes'))
    admin.add_view(AdminModelView(Category, db.session, endpoint='admin_category_view', name='Admin Categories'))
    
    # Mark admin initialization as complete
    app.admin_initialized = True
