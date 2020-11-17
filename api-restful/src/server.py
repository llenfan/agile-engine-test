from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
from flask import jsonify

import datetime
import time
import random
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
transactions = []
transaction_lock = False


def op_Locked():
    return transaction_lock


def get_balance():
    return sum((lambda v: t['amount'] if t['type'] == 'credit'
                else -t['amount'])(t) for t in transactions)


def is_valid_transaction(transaction):
    balance = get_balance()
    if transaction['type'] == 'debit' and balance < transaction['amount']:
        return False
    if transaction['amount'] < 0:
        return False
    return True


def cancel_if_locked():
    if op_Locked():
        abort(503, message="Locked")


def get_new_transcation_id():
    last_id = 1
    for t in transactions:
        if t['id'] > last_id:
            last_id = t['id']
    return last_id + 1


def get_transaction_by_id(transaction_id):
    for t in transactions:
        if t['id'] == transaction_id:
            return t
    return False


def add_transaction(tr_id, tr_type, amount, date):
    transaction = {}
    transaction['id'] = tr_id
    transaction['type'] = tr_type
    transaction['amount'] = amoun
t    transaction['effective_date'] = date

    if is_valid_transaction(transaction):
        transactions.insert(tr_id, transaction)
        return transaction
    abort(422, message="Error: insufficient balance or invalid amount")


def populate_transactions(initial_credit=500000, random_transactions=10):
    # Initial credit
    amount = initial_credit
    date = datetime.datetime.now().isoformat()
    add_transaction(1, 'credit', amount, date)

    # Random transactions
    for x in range(2, random_transactions):
        tr_type = 'credit'
        if (x % 2) == 0:
            tr_type = 'debit'

        amount = random.randint(10, 10000)
        date = datetime.datetime.now().isoformat()
        add_transaction(x, tr_type, amount, date)


class Balance(Resource):
    def get(self):
        return get_balance()


class TransactionsHistory(Resource):
    def get(self):
        resp = jsonify(transactions)
        return resp


class AddTransaction(Resource):
    def post(self):
        cancel_if_locked()
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True)
        parser.add_argument('amount', required=True)
        args = parser.parse_args()

        tr_id = get_new_transcation_id()
        tr_type = args['type']
        amount = int(args['amount'])
        date = datetime.datetime.now().isoformat()

        transaction_lock = True
        tr = add_transaction(tr_id, tr_type, amount, date)
        if tr:
            time.sleep(2)
            transaction_lock = False
            return tr, 201

        transaction_lock = False
        return {}, 422


class Transactions(Resource):
    def get(self, transaction_id):
        cancel_if_locked()
        transaction = get_transaction_by_id(int(transaction_id))
        if transaction:
            return transaction, 201
        else:
            abort(422, message="Transaction not found")

    def delete(self, transaction_id):
        return '', 500

    def put(self, transaction_id):
        return '', 500


api.add_resource(TransactionsHistory, '/transaction/history')
api.add_resource(Balance, '/transaction/balance')
api.add_resource(AddTransaction, '/transaction')
api.add_resource(Transactions, '/transaction/<transaction_id>')

# Actually setup the Api resources
if __name__ == '__main__':
    populate_transactions()
    app.run(debug=True, host='0.0.0.0', port=5001)
