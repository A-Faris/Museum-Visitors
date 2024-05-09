from pipeline import get_db_connection

conn = get_db_connection()


def run_sql_file(filename):
    """Runs the schema.sql file"""
    with open(filename, 'r', encoding='utf-8') as f:
        with conn.cursor() as cur:
            sql_commands = f.read().split(';')
            for command in sql_commands:
                try:
                    cur.execute(command)
                except Exception:
                    print(f"skipped {command}")
            data = cur.fetchall()
        conn.commit()
        return data


print(run_sql_file('schema.sql'))
