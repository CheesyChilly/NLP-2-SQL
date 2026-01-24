# backend/nlp/parser.py
import re

def parse_question(question: str) -> dict:
    q = question.lower()

    result = {
        "metric": None,
        "group_by": None,
        "filters": {}
    }

    # ---- METRIC ----
    if "total" in q and "revenue" in q:
        result["metric"] = "total_revenue"
    elif "total" in q and "budget" in q:
        result["metric"] = "total_budget"
    elif "total" in q and "hours" in q:
        result["metric"] = "total_salary"

    # ---- GROUP BY ----
    if "industry" in q:
        result["group_by"] = "industry"
    elif "region" in q:
        result["group_by"] = "region"
    elif "project" in q:
        result["group_by"] = "project_id"

    # ---- FILTERS ----
    for region in ["asia", "america", "europe"]:
        if region in q:
            result["filters"]["region"] = region.capitalize()

    for industry in ["bfsi", "retail", "manufacturing", "healthcare"]:
        if industry in q:
            result["filters"]["industry"] = industry.capitalize()

    year = re.search(r"\b(20\d{2})\b", q)
    if year:
        result["filters"]["year"] = int(year.group())

    quarter = re.search(r"\bq([1-4])\b", q)
    if quarter:
        result["filters"]["quarter"] = int(quarter.group(1))

    return result
