"""Seed the local database with an editable learning catalog."""

from __future__ import annotations

from sqlalchemy import select

from backend.app.core.config import get_settings
from backend.app.core.database import SessionLocal, init_db
from backend.app.core.security import hash_password
from backend.app.models import Problem, Resource, Topic, User, UserProfile
from backend.seed.problem_catalog import PROBLEM_CATALOG
from backend.seed.resource_catalog import RESOURCE_CATALOG
from backend.seed.topic_catalog import TOPIC_CATALOG, notes_for_topic


LANGUAGES = ("python", "cpp", "java", "javascript", "go", "csharp", "kotlin")


def starter_templates(title: str) -> dict[str, str]:
    return {
        "python": f"# {title}\ndef solve(input_data):\n    # Parse the input according to the linked problem statement.\n    return None\n",
        "cpp": f"// {title}\n#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {{\npublic:\n    void solve() {{\n        // Implement the invariant from your approach.\n    }}\n}};\n",
        "java": f"// {title}\nimport java.util.*;\n\nclass Solution {{\n    public void solve() {{\n        // Implement the invariant from your approach.\n    }}\n}}\n",
        "javascript": f"// {title}\nfunction solve(input) {{\n  // Parse input and maintain a clear invariant.\n  return null;\n}}\n",
        "go": f"// {title}\npackage main\n\nfunc solve(input []int) int {{\n\t// Implement the invariant from your approach.\n\treturn 0\n}}\n",
        "csharp": f"// {title}\nusing System;\n\npublic class Solution\n{{\n    public void Solve()\n    {{\n        // Implement the invariant from your approach.\n    }}\n}}\n",
        "kotlin": f"// {title}\nclass Solution {{\n    fun solve(input: IntArray): Int {{\n        // Implement the invariant from your approach.\n        return 0\n    }}\n}}\n",
    }


def approach_explanations(title: str, topic: str) -> dict[str, str]:
    base = (
        f"For {title}, first restate the input and output in your own words. "
        f"Use the {topic.replace('-', ' ')} invariant, test an empty and smallest input, "
        "then account for duplicate values and boundary indices. Record the time and space complexity before coding."
    )
    return {language: base for language in LANGUAGES}


def seed() -> dict[str, int]:
    init_db()
    database = SessionLocal()
    try:
        topics_by_slug: dict[str, Topic] = {}
        for data in TOPIC_CATALOG:
            topic = database.scalar(select(Topic).where(Topic.slug == data["slug"]))
            if topic is None:
                topic = Topic(slug=data["slug"], name=data["name"])
                database.add(topic)
            topic.name = data["name"]
            topic.order_index = data["order_index"]
            topic.color = data["color"]
            topic.prerequisites = data["prerequisites"]
            topic.description = data["description"]
            topic.notes_markdown = notes_for_topic(data["slug"], data["name"])
            topic.is_active = True
            database.flush()
            topics_by_slug[topic.slug] = topic

        problem_count = 0
        for topic_slug, entries in PROBLEM_CATALOG.items():
            topic = topics_by_slug[topic_slug]
            for title, difficulty, slug, tags, companies, minutes in entries:
                problem = database.scalar(select(Problem).where(Problem.slug == slug))
                if problem is None:
                    problem = Problem(slug=slug, topic_id=topic.id, title=title, difficulty=difficulty)
                    database.add(problem)
                problem.topic_id = topic.id
                problem.title = title
                problem.difficulty = difficulty
                problem.tags = tags
                problem.companies = companies
                problem.external_url = f"https://leetcode.com/problems/{slug}/"
                problem.estimated_minutes = minutes
                problem.prerequisites = topic.prerequisites
                problem.starter_templates = starter_templates(title)
                problem.approach_explanations = approach_explanations(title, topic_slug)
                problem.popularity_score = round(min(0.98, 0.48 + len(companies) * 0.06 + (0.08 if difficulty == "Medium" else 0.12 if difficulty == "Hard" else 0)), 2)
                problem.is_active = True
                problem_count += 1

        resource_count = 0
        for topic_slug, resources in RESOURCE_CATALOG.items():
            topic = topics_by_slug[topic_slug]
            for title, channel, url in resources:
                resource = database.scalar(
                    select(Resource).where(Resource.topic_id == topic.id, Resource.title == title)
                )
                if resource is None:
                    resource = Resource(topic_id=topic.id, title=title, channel=channel, url=url)
                    database.add(resource)
                resource.channel = channel
                resource.url = url
                resource.kind = "video" if "youtube" in url else "guide"
                resource.description = f"A curated {resource.kind} resource for {topic.name}. AlgoForge does not claim endorsement."
                resource_count += 1

        settings = get_settings()
        admin = database.scalar(select(User).where(User.email == settings.admin_email.lower()))
        if admin is None:
            admin = User(
                email=settings.admin_email.lower(),
                password_hash=hash_password(settings.admin_password),
                display_name="AlgoForge Admin",
                is_admin=True,
            )
            database.add(admin)
            database.flush()
            database.add(UserProfile(user_id=admin.id, onboarding_complete=True, goal="placements"))
        else:
            admin.is_admin = True
        database.commit()
        return {"topics": len(topics_by_slug), "problems": problem_count, "resources": resource_count}
    finally:
        database.close()


if __name__ == "__main__":
    print(seed())
