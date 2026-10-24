from backend.ml.sheet_generator import generate_day_plan, topological_topics


def test_topics_are_topologically_ordered() -> None:
    topics = [
        {"slug": "graphs", "name": "Graphs", "prerequisites": ["trees"], "order_index": 3},
        {"slug": "arrays", "name": "Arrays", "prerequisites": [], "order_index": 1},
        {"slug": "trees", "name": "Trees", "prerequisites": ["arrays"], "order_index": 2},
    ]
    ordered = [topic["slug"] for topic in topological_topics(topics)]
    assert ordered.index("arrays") < ordered.index("trees") < ordered.index("graphs")


def test_day_plan_respects_time_budget_and_does_not_repeat_problems() -> None:
    topics = [
        {"slug": "arrays", "name": "Arrays", "prerequisites": [], "order_index": 1},
        {"slug": "trees", "name": "Trees", "prerequisites": ["arrays"], "order_index": 2},
    ]
    problems = [
        {"id": str(index), "topic": "arrays", "title": f"Array {index}", "difficulty": "Easy", "estimated_minutes": 20}
        for index in range(1, 5)
    ] + [
        {"id": str(index), "topic": "trees", "title": f"Tree {index}", "difficulty": "Medium", "estimated_minutes": 25}
        for index in range(5, 9)
    ]
    plan = generate_day_plan(topics, problems, "placements", 6, 45, {"arrays": 0.3, "trees": 0.2})
    selected = [problem_id for day in plan for problem_id in day["problem_ids"]]
    assert selected
    assert len(selected) == len(set(selected))
    assert all(day["estimated_minutes"] <= 45 for day in plan)
    assert len(plan) <= 6
