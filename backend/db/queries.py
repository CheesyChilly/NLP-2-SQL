from db.connection import get_connection

def total_revenue_by_industry():
    query = """
    SELECT c.industry, SUM(r.revenue_amount_usd) AS total_revenue
    FROM revenue r
    JOIN projects p ON r.project_id = p.project_id
    JOIN clients c ON p.client_id = c.client_id
    GROUP BY c.industry
    ORDER BY total_revenue DESC;
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    conn.commit() 
    
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {"industry": industry, "total_revenue": float(revenue)}
        for industry, revenue in results
    ]
