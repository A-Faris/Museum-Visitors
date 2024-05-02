"""An API for handling marine experiments."""

from datetime import date
from flask import Flask, jsonify, request
# from psycopg2 import sql

from database_functions import get_db_connection, get_subject_info, get_experiment_info, \
    delete_experiment_info, post_experiment_info, get_subject_id_info


app = Flask(__name__)
conn = get_db_connection()


@app.route("/subject", methods=["GET"])
def get_subject() -> list:
    """Get subject"""
    return get_subject_info(conn)


@app.route("/experiment", methods=["GET"])
def get_experiment():
    """Get experiment"""
    type_name = request.args.get('type', "")
    score_over = request.args.get('score_over', "0")

    if not score_over.isdigit():
        return jsonify({"error": "score over is not an integer"}), 400
    if not 0 <= int(score_over) <= 100:
        return jsonify({"error": "score over is not between 0 and 100"}), 400
    if type_name and type_name not in ["intelligence", "obedience", "aggression"]:
        return jsonify({"error": "type isn't intelligence, obedience or aggression"}), 400

    return get_experiment_info(conn, type_name, int(score_over))


@app.route("/experiment/<int:experiment_id>", methods=["DELETE"])
def delete_experiment(experiment_id: int):
    """Delete experiment"""
    data = delete_experiment_info(conn, experiment_id)
    if not data:
        return jsonify({"error": "Experiment not found"}), 404
    return jsonify(data), 200


@app.route("/experiment", methods=["POST"])
def post_experiment():
    """Post experiment"""
    data = request.get_json()
    subject_id = data.get("subject_id")
    experiment_type = data.get("experiment_type")
    score = data.get("score")
    experiment_date = data.get("experiment_date", date.today().isoformat())

    if not any([subject_id, score, experiment_type]):
        return jsonify({"error": "Input needs subject_id, experiment_type and score"}), 400
    if experiment_type not in ["intelligence", "obedience", "aggression"]:
        return jsonify({"error": "Type isn't intelligence, obedience or aggression"}), 400
    if not isinstance(score, int):
        return jsonify({"error": "Score is not an integer"}), 400
    if experiment_type in ['obedience', 'aggression'] and not 0 <= score <= 10:
        return jsonify({"error": "Score isn't between 0 and 10"}), 400
    if experiment_type == "intelligence" and not 0 <= score <= 30:
        return jsonify({"error": "Score isn't between 0 and 30"}), 400
    try:
        date.fromisoformat(experiment_date)
    except ValueError:
        return jsonify({"error": "Incorrect data format, should be YYYY-MM-DD"}), 400

    data = post_experiment_info(conn, subject_id, experiment_type,
                                score, experiment_date)

    if not data:
        return jsonify({"error": "Subject not found"}), 404

    return jsonify(data), 201


@app.route("/subject/<int:subject_id>", methods=["GET"])
def get_subject_id(subject_id: int):
    """Get subject"""
    data = get_subject_id_info(conn, subject_id)
    if not data:
        return jsonify({"error": "Subject not found"}), 404
    return jsonify(data), 200


if __name__ == "__main__":
    app.run(port=8000, debug=True)
