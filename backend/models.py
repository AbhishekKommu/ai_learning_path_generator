import json
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(300), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paths = db.relationship("LearningPath", backref="owner", lazy=True,
                            cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class LearningPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    goal = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    hours_per_week = db.Column(db.Integer, default=5)
    total_weeks = db.Column(db.Integer, default=8)
    interests = db.Column(db.String(300), default="")
    plan_json = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(20), default="ml")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def plan(self):
        return json.loads(self.plan_json)

    def save_plan(self, plan):
        self.plan_json = json.dumps(plan)

    @property
    def progress(self):
        weeks = self.plan.get("weeks", [])
        if not weeks:
            return 0
        return round(100 * sum(1 for w in weeks if w.get("done")) / len(weeks))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
