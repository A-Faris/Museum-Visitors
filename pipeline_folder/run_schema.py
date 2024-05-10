from pipeline import get_db_connection

conn = get_db_connection()


def run_sql_file(filename):
    """Runs the schema.sql file"""
    f = open(filename, 'r', encoding='utf-8')
    sql_commands = f.read().split(';')
    f.close()

    cur = conn.cursor()
    for command in sql_commands:
        try:
            cur.execute(command)
        except Exception:
            print(f"skipped {command}")
    data = cur.fetchall()
    conn.commit()
    cur.close()

    return data


print(run_sql_file('schema.sql'))
