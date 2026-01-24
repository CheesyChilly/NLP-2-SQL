# backend/db/executor.py
from db.connection import get_connection

def run_query(sql: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
