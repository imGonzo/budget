import json
from random import randrange

import pandas as pd

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
