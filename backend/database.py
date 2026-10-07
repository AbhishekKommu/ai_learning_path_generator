import os
from extensions import db


def init_db(app):
    """Create the database folder and tables if they don't exist."""
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if uri.startswith("sqlite:///") and ":memory:" not in uri:
        os.makedirs(os.path.dirname(uri.replace("sqlite:///", "")), exist_ok=True)
    with app.app_context():
        from backend import models  # noqa: F401
        db.create_all()
