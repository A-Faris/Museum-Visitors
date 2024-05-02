"""Functions that interact with the database."""

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection(dbname="marine_experiments") -> connection:
    """Returns a DB connection"""
    return connect(dbname=dbname,
                   cursor_factory=RealDictCursor)


def get_subject_info(conn) -> list:
    """Get subject info"""
    cur = conn.cursor()

    cur.execute(
        """SELECT subject_id, subject_name, species_name,
        TO_CHAR(date_of_birth, 'YYYY-MM-DD') AS date_of_birth
        FROM subject
        JOIN species
        USING(species_id)
        ORDER BY date_of_birth DESC""")

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_experiment_info(conn, type_name: str, score_over: int) -> list:
    """Get experiment info"""
    cur = conn.cursor()

    if type_name:
        type_name = f"AND type_name = '{type_name}'"

    cur.execute(
        f"""SELECT experiment_id, subject_id, species_name AS species,
        TO_CHAR(experiment_date, 'YYYY-MM-DD') AS experiment_date,
        type_name AS experiment_type, ROUND(score/max_score*100, 2)::TEXT||'%' AS score
        FROM experiment
        JOIN subject USING(subject_id)
        JOIN species USING(species_id)
        JOIN experiment_type USING(experiment_type_id)
        WHERE score/max_score*100 > {score_over} {type_name}
        ORDER BY experiment_date DESC""")

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def delete_experiment_info(conn, experiment_id: int):
    """Delete experiment info"""
    cur = conn.cursor()
    # if subject id exists
    cur.execute(
        f"""DELETE FROM experiment
        WHERE experiment_id = {experiment_id}
        RETURNING experiment_id,
        TO_CHAR(experiment_date, 'YYYY-MM-DD') AS experiment_date""")

    data = cur.fetchone()
    conn.commit()
    cur.close()
    return data


def post_experiment_info(conn, subject_id, experiment_type, score, experiment_date):
    """Post experiment info"""
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO experiment(subject_id, experiment_date, score, experiment_type_id)
        SELECT %s, %s, %s, experiment_type_id
        FROM experiment_type
        WHERE type_name = %s
        AND EXISTS (SELECT 1 FROM subject WHERE subject_id = %s)
        RETURNING *, TO_CHAR(experiment_date, 'YYYY-MM-DD') AS experiment_date""",
        (subject_id, experiment_date, score, experiment_type, subject_id))

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_subject_id_info(conn, subject_id):
    """Get subject ID info"""
    cur = conn.cursor()

    cur.execute(
        f"""SELECT subject_id, subject_name, COUNT(experiment) AS total_experiment,
        TO_CHAR(date_of_birth, 'YYYY-MM-DD') AS date_of_birth, MIN(species_name) AS species_name
        FROM subject
        JOIN experiment USING(subject_id)
        JOIN species USING(species_id)
        JOIN experiment_type USING(experiment_type_id)
        WHERE subject_id = {subject_id}
        GROUP BY subject_id""")

    data = cur.fetchone()

    for type_name in ['intelligence', 'obedience', 'aggression']:
        cur.execute(
            f"""SELECT ROUND(AVG(score)/max_score*100, 2)::TEXT||'%' AS avg_{type_name}_score
            FROM experiment
            JOIN experiment_type USING(experiment_type_id)
            WHERE subject_id = {subject_id} and type_name = '{type_name}'
            GROUP BY subject_id, max_score""")
        score = cur.fetchone()
        if score:
            data.update(score)

    conn.commit()
    cur.close()
    return data
