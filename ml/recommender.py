"""Offline learning-path recommender: TF-IDF matches a goal to a career track,
then skills are ordered by level and spread across the available weeks."""
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_DATA_FILE = os.path.join(os.path.dirname(__file__), "career_data.json")
_LEVEL_ORDER = {"beginner": 0, "intermediate": 1, "advanced": 2}


def _load():
    with open(_DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def match_career(goal, interests=""):
    careers = _load()
    docs = [c["career"] + " " + c["keywords"] for c in careers]
    vec = TfidfVectorizer(stop_words="english")
    matrix = vec.fit_transform(docs + [f"{goal} {goal} {interests}"])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    return careers[int(scores.argmax())]


def build_plan(goal, level, hours_per_week, total_weeks, interests=""):
    career = match_career(goal, interests)
    start = _LEVEL_ORDER.get(level, 0)
    skills = [s for s in career["skills"] if _LEVEL_ORDER[s["level"]] >= start]
    skills.sort(key=lambda s: _LEVEL_ORDER[s["level"]])
    if not skills:
        skills = career["skills"][-2:]

    total_weeks = max(2, int(total_weeks))
    weeks = []
    for i in range(total_weeks - 1):
        s = skills[min(len(skills) - 1, i * len(skills) // (total_weeks - 1))]
        weeks.append(s)

    plan_weeks, seen = [], {}
    for i, s in enumerate(weeks, 1):
        seen[s["topic"]] = seen.get(s["topic"], 0) + 1
        part = f" (part {seen[s['topic']]})" if seen[s["topic"]] > 1 else ""
        plan_weeks.append({
            "week": i, "title": s["topic"] + part,
            "topics": [f"Study: {s['topic']}", f"Practice about {hours_per_week} hours this week",
                       "Write down 3 things you learned"],
            "resources": s["resources"], "done": False,
        })
    plan_weeks.append({
        "week": total_weeks, "title": "Capstone project & review",
        "topics": [f"Build a small project that proves your {career['career']} skills",
                   "Publish it on GitHub with a clear README", "List gaps to work on next"],
        "resources": ["GitHub Pages", "Your own portfolio"], "done": False,
    })
    return {
        "title": f"{career['career']} path: {total_weeks} weeks",
        "career": career["career"],
        "summary": (f"A {level}-level plan toward '{goal}', matched to the {career['career']} track, "
                    f"at {hours_per_week} hours per week."),
        "notes": "", "weeks": plan_weeks,
    }
