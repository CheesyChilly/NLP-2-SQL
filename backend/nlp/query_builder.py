# backend/db/query_builder.py
FORBIDDEN = ["drop", "delete", "truncate", "alter", ";--", "';--", "\";--"]
METRIC_MAP = {
    "total_revenue": {
        "base_table": "revenue",
        "column": "revenue_amount_usd",
        "joins": []
    },
    "total_budget": {
        "base_table": "projects",
        "column": "revenue_amount_usd",
        "joins": [
            ("revenue", "projects.project_id = revenue.project_id")
        ]
    }
}

def build_sql(parsed: dict) -> str:
    metric = parsed["metric"]
    group_by = parsed["group_by"]
    filters = parsed["filters"]

    if metric not in METRIC_MAP:
        raise ValueError(f"Unsupported metric: {metric}")


    config = METRIC_MAP[metric]
    base_table = config["base_table"]
    column = config["column"]
    joins = config["joins"]

    # ---- SELECT ----
    if group_by:
        sql = f"SELECT {group_by}, SUM({column}) AS {metric}"
    else:
        sql = f"SELECT SUM({column}) AS {metric}"

    # ---- FROM ----
    sql += f" FROM {base_table}"

    # ---- JOINS ----
    for table, condition in joins:
        sql += f" JOIN {table} ON {condition}"

    # ---- WHERE ----
    conditions = []

    for k, v in filters.items():
        if k == "year":
            conditions.append(f"EXTRACT(YEAR FROM revenue_date) = {v}")
        elif k == "quarter":
            conditions.append(f"EXTRACT(QUARTER FROM revenue_date) = {v}")
        else:
            conditions.append(f"{k} = '{v}'")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    # ---- GROUP BY ----
    if group_by:
        sql += f" GROUP BY {group_by}"

    sql = sql + ";"

    if any(word in sql.lower() for word in FORBIDDEN):
        raise ValueError("Unsafe SQL detected")


    if not sql:
        raise ValueError("Unsupported query")

    return sql