from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, migrate, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from backend.auth import auth_bp
    from backend.routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    from backend.database import init_db
    init_db(app)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
