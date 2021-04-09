
from io import BytesIO
import json

from flask import Flask, session, url_for, redirect, request, Response, jsonify

from budget.statement import Statement

app = Flask(__name__)

@app.route('/statement', methods=["GET"])
def get_statements():
    return jsonify(Statement.get_statements())

@app.route('/statement', methods=["POST"])
def create_statement():
    date = request.args.get('date')
    doc = Statement.get_statement({"Date": date})
    file = request.get_data()

    if doc:
        return "statement already exists with the date {}".format(date), 400

    statement = Statement.from_file(file, date)
    statement.save()

    return jsonify(statement.doc)

@app.route('/statement/<statement_id>', methods=["PATCH"])
def update_statement(statement_id):
    trusted_doc = Statement.get_statement({"_id": "statement:{}".format(statement_id)})
    doc = request.json

    if not trusted_doc:
        return "statement {} does not exist".format(statement_id), 404
    elif not doc:
        return "no payload provided", 400
    elif doc['_id'] != trusted_doc['_id']:
        return "statement_id mismatch", 400

    statement = Statement(trusted_doc)
    statement.update_statement(doc)

    return jsonify(statement.doc)
