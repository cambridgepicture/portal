from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from config import LOGIN_PASSWORD, LOGIN_USERNAME, SECRET_KEY, STATIC_URL_PATH
from shared.auth import current_user, get_user_store, require_admin, require_login, visible_apps_for_user
from shared import install_shared_header

APP_CATALOG = {
    'contracts': {
        'slug': 'contracts',
        'title': 'Contracts',
        'description': 'Generate contract documents from approved templates.',
        'badge': 'Available now',
        'url': '/contracts',
    },
    'news': {
        'slug': 'news',
        'title': 'News',
        'description': 'Review the latest digest and manage saved stories.',
        'badge': 'Available now',
        'url': '/news',
    },
    'tasks': {
        'slug': 'tasks',
        'title': 'Tasks',
        'description': 'Track work, projects, and daily focus items.',
        'badge': 'Available now',
        'url': '/tasks',
    },
    'translate': {
        'slug': 'translate',
        'title': 'Translator',
        'description': 'Upload DOCX files and generate bilingual or Chinese-only outputs.',
        'badge': 'Available now',
        'url': '/translate',
    },
}


def create_app() -> Flask:
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path=STATIC_URL_PATH)
    app.config.update(SECRET_KEY=SECRET_KEY, PREFERRED_URL_SCHEME='https')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    install_shared_header(app, auth_enabled=True)

    user_store = get_user_store()
    if user_store.count_users() == 0 and LOGIN_USERNAME and LOGIN_PASSWORD:
        user_store.seed_admin(email=LOGIN_USERNAME, password=LOGIN_PASSWORD, allowed_apps=APP_CATALOG.keys())

    @app.before_request
    def load_current_user():
        current_user()

    @app.context_processor
    def inject_shared_context():
        return {
            "current_user": current_user(),
            "shared_auth_enabled": True,
        }

    @app.get('/')
    @require_login
    def home():
        user = current_user()
        return render_template('home.html', user=user, apps=visible_apps_for_user(user, APP_CATALOG))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user() is not None:
            return redirect(url_for('home'))
        next_url = request.values.get('next') or url_for('home')
        if request.method == 'POST':
            user = get_user_store().authenticate(request.form.get('username', ''), request.form.get('password', ''))
            if user is not None:
                session.clear()
                session['user_id'] = user['user_id']
                return redirect(next_url if next_url.startswith('/') and not next_url.startswith('//') else url_for('home'))
            flash('Invalid username or password.', 'error')
        return render_template('login.html', next_url=next_url)

    @app.get('/logout')
    @require_login
    def logout():
        session.clear()
        flash('You have been signed out.', 'message')
        return redirect(url_for('login'))

    @app.get('/admin')
    @require_admin
    def admin_dashboard():
        return render_template('admin.html', user=current_user(), users=user_store.list_users(), available_apps=list(APP_CATALOG.values()))

    @app.post('/admin/users')
    @require_admin
    def create_user():
        try:
            user_store.create_user(email=request.form.get('email', ''), password=request.form.get('password', ''), is_admin=request.form.get('is_admin') == 'on', allowed_apps=request.form.getlist('allowed_apps'))
            flash(f"Added user {request.form.get('email','').strip().lower()}.", 'message')
        except Exception as exc:  # noqa: BLE001
            flash(str(exc), 'error')
        return redirect(url_for('admin_dashboard'))

    @app.post('/admin/users/<int:user_id>')
    @require_admin
    def update_user(user_id: int):
        try:
            user_store.update_user(user_id, email=request.form.get('email', ''), password=(request.form.get('password', '').strip() or None), is_admin=request.form.get('is_admin') == 'on', allowed_apps=request.form.getlist('allowed_apps'))
            flash('User updated.', 'message')
        except Exception as exc:  # noqa: BLE001
            flash(str(exc), 'error')
        return redirect(url_for('admin_dashboard'))

    return app


app = create_app()
