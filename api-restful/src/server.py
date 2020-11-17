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

aux_transac = {'id': 0, 'lock': False}

transactions = []

for x in range (0, 50):
    transaction_type = 'credit'
    transaction_amount = random.randint(0, 10000)
    transac_date = datetime.datetime.now().isoformat()

    if (x % 2) == 0:
        transaction_type = 'debit'

    transactions.append({'type': transaction_type, 
                        'amount': transaction_amount, 
                        'effective_date': transac_date})

def op_Locked():
    return aux_transac['lock']

def cancel_if_locked():
    if op_Locked():
        abort(404, message="Locked!")

class Balance(Resource):
    def get(self):
        sumat = sum((lambda v: v['amount'] if v['type'] == 'credit' else -v['amount'])(v)  for (k,v) in transactions.items())
        return sumat

class TransactionsHistory(Resource):
    def get(self):
        #resp = [{'id': k, **v} for (k,v) in transactions.items()]
        resp = jsonify(transactions)
        return resp

class AddTransaction(Resource):
    def post(self):
    
        cancel_if_locked()

        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True)
        parser.add_argument('amount', required=True)
        args = parser.parse_args()

        current_transac_id = aux_transac['id']
        current_transac_id = current_transac_id + 1
        aux_transac['id'] = current_transac_id
        
        aux_transac['lock'] = True

        transactions[current_transac_id] = {'type' : args['type'], 'amount': args['amount'], 'effectiveDate': datetime.datetime.now().isoformat()}
        
        time.sleep(5)  # a wide window of time to help tests

        aux_transac['lock'] = False

        resp = {'id' : current_transac_id, **transactions[current_transac_id]}
        
        return resp, 201

class Transactions(Resource):
    def get(self, transaction_id):
        
        cancel_if_locked()

        resp = {'id' : transaction_id, **transactions[transaction_id]}
        return resp, 201

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
    
