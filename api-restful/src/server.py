from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin

import datetime
import time
import random
import json
from flask import jsonify

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

transaction_lock = False

def op_Locked():
    return transaction_lock

def get_balance():
    return sum((lambda v: t['amount'] if t['type'] == 'credit' else -t['amount'])(t)  for t in transactions)

def is_valid_transaction(transaction):
    balance = get_balance()
    if transaction['type'] == 'debit' and balance < transaction['amount']:
        return False
    if transaction['amount'] < 0:
        return False

    return True

def cancel_if_locked():
    if op_Locked():
        abort(404, message="Locked!")

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



transactions = []

for x in range (1, 50):
    transaction_type = 'credit'
    if (x % 2) == 0:
        transaction_type = 'debit'

    transaction = {'id': x,
                    'type': transaction_type, 
                    'amount': random.randint(10, 10000), 
                    'effective_date': datetime.datetime.now().isoformat()}

    if is_valid_transaction(transaction):
        transactions.append(transaction)

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
        transaction_id = get_new_transcation_id()

        transaction_lock = True

        new_transaction =  {'id': transaction_id, 
                            'type' : args['type'], 
                            'amount': int(args['amount']), 
                            'effective_date': datetime.datetime.now().isoformat()}
        if is_valid_transaction(new_transaction):
            transactions.insert(transaction_id, new_transaction)
            time.sleep(2) 
            transaction_lock = False
            return new_transaction, 201
            
        transaction_lock = False
        return {}, 422
        
        
class Transactions(Resource):
    def get(self, transaction_id):
        
        cancel_if_locked()
        transaction = get_transaction_by_id(int(transaction_id))
        if transaction:
            return transaction, 201
        else:
            return {}, 422

    def delete(self, transaction_id):
        return '', 500

    def put(self, transaction_id):
        return '', 500


##
## Actually setup the Api resource routing here
##

api.add_resource(TransactionsHistory, '/transaction/history')
api.add_resource(Balance, '/transaction/balance')
api.add_resource(AddTransaction, '/transaction')
api.add_resource(Transactions, '/transaction/<transaction_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
    
