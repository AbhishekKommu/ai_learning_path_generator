from ml.recommender import build_plan, match_career
from backend.ai_engine import generate_learning_path


def test_match_career():
    assert "Machine Learning" in match_career("I want to build machine learning models")["career"]


def test_plan_has_requested_weeks():
    plan = build_plan("data analyst", "beginner", 5, 8)
    assert len(plan["weeks"]) == 8
    assert plan["weeks"][-1]["title"].startswith("Capstone")


def test_fallback_source(app):
    plan, source = generate_learning_path("web developer", "beginner", 5, 4)
    assert source == "ml" and plan["weeks"]
