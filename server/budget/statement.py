from io import BytesIO
import json
import uuid
from random import randrange

import pandas as pd

import db

def _statement_data():
    return db.cn['statement_data']

#!!!TBD!!! Should be BankStatement or BudgetStatement?
class Statement:
    SAFE_CATEGORIES = ["wants", "needs", "savings"]
    
    @classmethod
    def from_file(cls, file, date) -> 'Statement':
        statement = ExcelStatement(BytesIO(file))
        doc = {
            "_id": 'statement:{}'.format(uuid.uuid4()),
            "Date": date,
            "Budget": [],
            "Transactions": statement.transactions
        }

        for transaction in doc["Transactions"]:
            transaction["_id"] = 'transaction:{}'.format(uuid.uuid4())
            transaction["Category"] = None

        return cls(doc)

    @classmethod
    def get_statement(cls, query):
        return _statement_data().find_one(query) or None

    @classmethod
    def get_statements(cls):
        return [statement for statement in _statement_data().find()]

    @property
    def doc(self):
        return self._doc
        
    @property
    def transactions(self):
        return self._doc["Transactions"]

    def __init__(self, statement_doc):
        self._doc = json.loads(json.dumps(statement_doc))

    def _update_statement_transaction(self, transaction_id, category):
        for transaction in self._doc['Transactions']:
            if transaction["_id"] == transaction_id:
                transaction["Category"] = category

    def save(self):
        _statement_data().update({"_id": self._doc['_id']}, self._doc)

    def update_statement(self, statement_doc):
        for transaction in statement_doc["Transactions"]:
            category = transaction["Category"] or None
            transaction_id = transaction["_id"]

            if category:
                self._update_statement_transaction(transaction_id, category)
        
        self.save()

class ExcelStatement:
    def __init__(self, file=None):
        self._statement = pd.read_csv(file, index_col=False, encoding="latin1")
        self._statement.columns = self._statement.columns.str.replace(' ', '')
        del self._statement['CheckorSlip#']

    @property
    def to_json(self):
        if hasattr(self, "_json"):
            return self._json

        self._json = self._statement.to_json(orient='records')

        return self._json

    @property
    def to_dict(self):
        if hasattr(self, "_dict"):
            return self._dict

        self._dict = self._statement.to_dict(orient='records')

        return self._dict
    
    @property
    def debits(self):
        return  [trans for trans in self.to_dict if trans["Details"] == "DEBIT"]

    @property
    def transactions(self):
        return  self.to_dict 



# def updateTransactionCategory(transaction_id, category):
#     for tansaction in doc:
#         if transaction["_id"] == transaction_id:
#             transaction["Category"] = category

# def calcCategoryTotal(category):
#     total = 0

#     for transaction in doc:
#         if transaction["Category"] is category and transaction["Details"] == "DEBIT":
#             total += transaction["Amount"]

#     return round(abs(total))

# def calcSavings():
#     savings = calcCategoryTotal("want") + calcCategoryTotal("need")
#     savings = total_income - savings

#     return savings


# categories = {
#     "want": .3,
#     "need": .5,
#     "savings": .2
# }

# for transaction in doc:
#     updateTransactionCategory(transaction["_id"], list(categories.keys())[randrange(2)])

# total_income = 5380
# expected_spent = {}

# for category, rate in categories.items():
#     expected_spent[category] = total_income * rate
