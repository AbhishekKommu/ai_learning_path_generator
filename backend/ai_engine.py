"""Generates a learning path. Uses the Anthropic API when a key is set;
falls back to the scikit-learn recommender otherwise (or if the API fails)."""
import json
import re
import requests
from flask import current_app
from ml.recommender import build_plan

API_URL = "https://api.anthropic.com/v1/messages"


def _llm_plan(goal, level, hours, weeks, interests):
    prompt = (
        f"Create a {weeks}-week learning plan.\nGoal: {goal}\nLevel: {level}\n"
        f"Hours per week: {hours}\nExisting skills/interests: {interests or 'none'}\n\n"
        "Reply with ONLY valid JSON in this shape:\n"
        '{"title": str, "career": str, "summary": str, "weeks": [{"week": int, "title": str, '
        '"topics": [str], "resources": [str]}]}\n'
        f"Include exactly {weeks} weeks. Prefer free, well-known resources."
    )
    resp = requests.post(
        API_URL,
        headers={"x-api-key": current_app.config["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={"model": current_app.config["AI_MODEL"], "max_tokens": 4000,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=60,
    )
    resp.raise_for_status()
    text = "".join(b.get("text", "") for b in resp.json()["content"])
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    plan = json.loads(text)
    for i, w in enumerate(plan["weeks"], 1):
        w["week"] = i
        w["done"] = False
        w.setdefault("topics", [])
        w.setdefault("resources", [])
    plan.setdefault("notes", "")
    return plan


def generate_learning_path(goal, level, hours_per_week, total_weeks, interests=""):
    """Returns (plan_dict, source) where source is 'llm' or 'ml'."""
    if current_app.config.get("ANTHROPIC_API_KEY"):
        try:
            return _llm_plan(goal, level, hours_per_week, total_weeks, interests), "llm"
        except Exception as exc:  # network, JSON, or API errors -> fallback
            current_app.logger.warning("LLM generation failed, using ML fallback: %s", exc)
    return build_plan(goal, level, hours_per_week, total_weeks, interests), "ml"
