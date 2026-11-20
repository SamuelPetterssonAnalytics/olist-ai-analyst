from db import get_connection
from sql_validator import validate_sql


def execute_query(sql):
    valid, message = validate_sql(sql)

    if not valid:
        raise ValueError(message)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)

            columns = [description.name for description in cursor.description]
            rows = cursor.fetchall()

    return columns, rows