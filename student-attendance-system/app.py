import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from config import config
from database import db, init_db, User

login_manager = LoginManager()


def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    init_db(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from auth import auth_bp
    from api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Main routes
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return render_template('admin/dashboard.html')
        elif current_user.role == 'teacher':
            return render_template('teacher/dashboard.html')
        else:
            return render_template('parent/dashboard.html')

    # Admin routes
    @app.route('/admin/users')
    @login_required
    def admin_users():
        from auth.utils import admin_required
        users = User.query.all()
        return render_template('admin/users.html', users=users)

    @app.route('/admin/classes')
    @login_required
    def admin_classes():
        from database import Class
        classes = Class.query.all()
        return render_template('admin/classes.html', classes=classes)

    # Teacher routes
    @app.route('/teacher/attendance')
    @login_required
    def teacher_attendance():
        return render_template('teacher/attendance.html')

    @app.route('/teacher/journal')
    @login_required
    def teacher_journal():
        return render_template('teacher/journal.html')

    # Parent routes
    @app.route('/parent/attendance')
    @login_required
    def parent_attendance():
        return render_template('parent/attendance.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app


# CLI commands
def register_commands(app):
    """Register CLI commands"""

    @app.cli.command('create-admin')
    def create_admin():
        """Create default admin user"""
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print('Admin user already exists!')
            return

        admin = User(
            username='admin',
            email='admin@school.local',
            full_name='Administrator',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin user created! Username: admin, Password: admin123')

    @app.cli.command('init-db')
    def init_database():
        """Initialize database"""
        db.create_all()
        print('Database initialized!')


app = create_app()
register_commands(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
