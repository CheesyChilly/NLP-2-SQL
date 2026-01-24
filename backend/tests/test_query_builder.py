# backend/tests/test_query_builder.py
from nlp.query_builder import build_sql

def test_sql_generation():
    parsed = {
        "metric": "total_revenue",
        "group_by": "industry",
        "filters": {"region": "Asia", "year": 2024, "quarter": 2}
    }

    sql = build_sql(parsed)

    expected = (
        "SELECT industry, SUM(revenue_amount_usd) AS total_revenue "
        "FROM revenue "
        "WHERE region = 'Asia' "
        "AND EXTRACT(YEAR FROM revenue_date) = 2024 "
        "AND EXTRACT(QUARTER FROM revenue_date) = 2 "
        "GROUP BY industry;"
    )

    assert sql.replace(" ", "") == expected.replace(" ", "")
