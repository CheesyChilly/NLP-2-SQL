# backend/tests/test_pipeline.py
from nlp.parser import parse_question
from nlp.query_builder import build_sql
from db.queries import run_query

def test_end_to_end():
    q = "Total revenue by industry in Q2 2024 for Asia"
    parsed = parse_question(q)
    sql = build_sql(parsed)
    result = run_query(sql)

    assert len(result) > 0
    assert isinstance(result[0][1], (int, float))
