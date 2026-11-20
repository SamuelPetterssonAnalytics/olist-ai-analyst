import sqlglot
from sqlglot import exp


ALLOWED_VIEWS = {
    "ai_orders",
    "ai_order_items",
    "ai_reviews",
}


def validate_sql(sql):
    if sql.strip() == "CANNOT_ANSWER":
        return False, "Question cannot be answered from available data."

    try:
        statements = sqlglot.parse(sql, read="postgres")
    except Exception:
        return False, "SQL could not be parsed."

    if len(statements) != 1:
        return False, "Only one SQL statement is allowed."

    statement = statements[0]

    if not isinstance(statement, exp.Query):
        return False, "Only read-only SELECT queries are allowed."

    # Collect CTE names such as customer_orders
    cte_names = {
        cte.alias_or_name
        for cte in statement.find_all(exp.CTE)
    }

    # Check referenced tables/views
    for table in statement.find_all(exp.Table):
        table_name = table.name

        if table_name in cte_names:
            continue

        if table_name not in ALLOWED_VIEWS:
            return False, f"Access to '{table_name}' is not allowed."

    return True, "SQL is valid."