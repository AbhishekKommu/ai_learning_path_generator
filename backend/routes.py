from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from extensions import db
from backend.models import LearningPath
from backend.forms import GenerateForm, EditForm, ProfileForm
from backend.ai_engine import generate_learning_path

main_bp = Blueprint("main", __name__)


def _own_path(path_id):
    path = db.session.get(LearningPath, path_id)
    if not path or path.user_id != current_user.id:
        abort(404)
    return path


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    paths = (LearningPath.query.filter_by(user_id=current_user.id)
             .order_by(LearningPath.created_at.desc()).all())
    return render_template("dashboard/dashboard.html", paths=paths)


@main_bp.route("/generate", methods=["GET", "POST"])
@login_required
def generate():
    form = GenerateForm()
    if form.validate_on_submit():
        plan, source = generate_learning_path(
            goal=form.goal.data.strip(), level=form.level.data,
            hours_per_week=form.hours_per_week.data, total_weeks=form.total_weeks.data,
            interests=(form.interests.data or "").strip(),
        )
        path = LearningPath(
            user_id=current_user.id, title=plan.get("title", form.goal.data),
            goal=form.goal.data.strip(), level=form.level.data,
            hours_per_week=form.hours_per_week.data, total_weeks=form.total_weeks.data,
            interests=(form.interests.data or "").strip(), source=source,
            plan_json="{}",
        )
        path.save_plan(plan)
        db.session.add(path)
        db.session.commit()
        return redirect(url_for("main.result", path_id=path.id))
    return render_template("learning_path/generate.html", form=form)


@main_bp.route("/path/<int:path_id>/result")
@login_required
def result(path_id):
    return render_template("learning_path/result.html", path=_own_path(path_id))


@main_bp.route("/path/<int:path_id>")
@login_required
def view_path(path_id):
    return render_template("learning_path/view.html", path=_own_path(path_id))


@main_bp.route("/path/<int:path_id>/edit", methods=["GET", "POST"])
@login_required
def edit_path(path_id):
    path = _own_path(path_id)
    form = EditForm(title=path.title, notes=path.plan.get("notes", ""))
    if form.validate_on_submit():
        plan = path.plan
        plan["title"] = form.title.data.strip()
        plan["notes"] = form.notes.data or ""
        path.title = plan["title"]
        path.save_plan(plan)
        db.session.commit()
        flash("Changes saved.", "success")
        return redirect(url_for("main.view_path", path_id=path.id))
    return render_template("learning_path/edit.html", form=form, path=path)


@main_bp.route("/path/<int:path_id>/delete", methods=["POST"])
@login_required
def delete_path(path_id):
    db.session.delete(_own_path(path_id))
    db.session.commit()
    flash("Learning path deleted.", "info")
    return redirect(url_for("main.dashboard"))


@main_bp.route("/path/<int:path_id>/toggle/<int:week>", methods=["POST"])
@login_required
def toggle_week(path_id, week):
    path = _own_path(path_id)
    plan = path.plan
    for w in plan.get("weeks", []):
        if w["week"] == week:
            w["done"] = not w.get("done", False)
            path.save_plan(plan)
            db.session.commit()
            return jsonify(done=w["done"], progress=path.progress)
    abort(404)


@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data.strip()
        current_user.bio = form.bio.data or ""
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("main.profile"))
    return render_template("profile/profile.html", form=form)
