from db.queries import total_revenue_by_industry

if __name__ == "__main__":
    data = total_revenue_by_industry()

    for row in data:
        print(row)
