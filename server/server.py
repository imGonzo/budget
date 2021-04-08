
from io import BytesIO
import json
import uuid

from flask import Flask, session, url_for, redirect, request, Response, jsonify

import db
from budget.excelstatement import ExcelStatement

app = Flask(__name__)

def _statement_data():
    return db.cn['statement_data']

@app.route('/statement', methods=["POST"])
def create_statement():
    date = request.args.get('date')
    doc = _statement_data().find({"Date": date})
    file = request.get_data()

    if doc:
        return "Statement already exists for the date {}".format(date), 400

    statement = ExcelStatement(BytesIO(file))
    
    doc = {
        "_id": 'statement:%s' % uuid.uuid4(),
        "Date": date,
        "Budget": [],
        "Transactions": statement.transactions
    }

    for transaction in doc["Transactions"]:
        transaction["_id"] = 'transaction:{}'.format(uuid.uuid4())
        transaction["Category"] = None

    _statement_data().insert_one(doc)
    return json.dumps(doc, indent=4)

@app.route('/statement/<statement_id>', methods=["POST"])
def update_statement(statement_id):
    return 'updating statement'
