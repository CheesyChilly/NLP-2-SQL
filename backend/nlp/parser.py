import re

def parse_question(question: str) -> dict:
    """
    Parse a natural language question into structured intent for SQL generation.
    Returns a dictionary with:
        - metric: the aggregate or measure requested
        - group_by: dimension to group results by
        - filters: optional filtering conditions
    """
    q = question.lower()
    
    result = {
        "metric": None,
        "group_by": None,
        "filters": {}  # e.g., {"region": "Asia", "industry": "BFSI"}
    }

    # ====================
    # METRIC DETECTION
    # ====================
    if re.search(r"\btotal\b.*\brevenue\b", q):
        result["metric"] = "total_revenue"
    elif re.search(r"\btotal\b.*\bsalary\b", q):
        result["metric"] = "total_salary"
    elif re.search(r"\btotal\b.*\bbudget\b", q):
        result["metric"] = "total_budget"

    # ====================
    # GROUP BY DETECTION
    # ====================
    if "by industry" in q:
        result["group_by"] = "industry"
    elif "by region" in q:
        result["group_by"] = "region"
    elif "by project" in q:
        result["group_by"] = "project_id"
    elif "by client" in q:
        result["group_by"] = "client_id"
    elif "by employee" in q:
        result["group_by"] = "employee_id"

    # ====================
    # FILTER EXTRACTION
    # ====================
    regions = ["asia", "america", "europe"]
    industries = ["bfsi", "retail", "manufacturing", "healthcare"]

    for r in regions:
        if r in q:
            result["filters"]["region"] = r.capitalize()
            break

    for i in industries:
        if i in q:
            result["filters"]["industry"] = i.capitalize()
            break

    # Optional: numeric filters (e.g., year, quarter)
    year_match = re.search(r"(?:in|for)\s+(\d{4})", q)
    if year_match:
        result["filters"]["year"] = int(year_match.group(1))

    quarter_match = re.search(r"q([1-4])", q)
    if quarter_match:
        result["filters"]["quarter"] = int(quarter_match.group(1))

    return result
