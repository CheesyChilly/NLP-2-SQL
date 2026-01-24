# backend/tests/test_parser.py
from nlp.parser import parse_question

def test_total_revenue_by_industry():
    q = "Total revenue by industry in Q2 2024 for Asia"
    parsed = parse_question(q)

    assert parsed["metric"] == "total_revenue"
    assert parsed["group_by"] == "industry"
    assert parsed["filters"]["region"] == "Asia"
    assert parsed["filters"]["year"] == 2024
    assert parsed["filters"]["quarter"] == 2
