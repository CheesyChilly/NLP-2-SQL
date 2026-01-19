def build_sql(parsed_data: dict) -> str:
    """
    Generate SQL query from parsed data dictionary.
    Handles metric, optional group_by, and filters.
    """
    metric = parsed_data.get("metric")
    group_by = parsed_data.get("group_by")
    filters = parsed_data.get("filters", {})

    # ======= MAP METRICS TO TABLES & COLUMNS =======
    metric_map = {
    "total_revenue": {
        "table": "revenue",
        "column": "revenue_amount_usd",
        "join": None  # no join needed
    },
    "total_salary": {
        "table": "employees",
        "column": "billable_hours",
        "join": None
    },
    "total_budget": {
        "table": "projects",
        "column": "revenue_amount_usd",  # actual revenue is in revenue table
        "join": {
            "table": "revenue",
            "on": "projects.project_id = revenue.project_id",
            "column": "revenue_amount_usd"
        }
    }
}

    if metric not in metric_map:
        return ""  # unsupported metric

    table, column = metric_map[metric]

    # ======= BUILD BASE SQL =======
    sql = f"SELECT "

    if group_by:
        sql += f"{group_by}, SUM({column}) AS {metric}"
    else:
        sql += f"SUM({column}) AS {metric}"

    sql += f" FROM {table}"

    # ======= ADD FILTERS =======
    where_clauses = []

    for key, value in filters.items():
        if key == "year" and table == "revenue":
            where_clauses.append(f"EXTRACT(YEAR FROM revenue_date) = {value}")
        elif key == "quarter" and table == "revenue":
            where_clauses.append(f"EXTRACT(QUARTER FROM revenue_date) = {value}")
        elif key in ["region", "industry", "client_id", "project_id", "employee_id"]:
            # Assume column exists in table
            where_clauses.append(f"{key} = '{value}'")

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    # ======= ADD GROUP BY =======
    if group_by:
        sql += f" GROUP BY {group_by}"

    sql += ";"

    return sql
