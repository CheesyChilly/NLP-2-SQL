# backend/main.py
from nlp.parser import parse_question
from nlp.query_builder import build_sql
from db.queries import run_query

if __name__ == "__main__":
    question = "Total revenue by industry in Q2 2024 for Asia"

    parsed = parse_question(question)
    sql = build_sql(parsed)
    result = run_query(sql)

    print("Parsed:", parsed)
    print("SQL:", sql)
    print("Result:", result)
