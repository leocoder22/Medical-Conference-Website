from datetime import datetime
from flask import Flask

from app.config import Config
from app.extensions import db, login_manager, mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.main import main_bp
    from app.auth import auth_bp
    from app.user import user_bp
    from app.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.context_processor
    def inject_config():
        return {"config": app.config}

    with app.app_context():
        db.create_all()

    @app.template_filter("ampm")
    def format_time_ampm(value):
        if not value:
            return ""

        try:
            return datetime.strptime(value, "%H:%M").strftime("%I:%M %p")
        except Exception:
            return value

    return app