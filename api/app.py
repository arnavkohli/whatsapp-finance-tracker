from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

import json

from db_managers import UserDBManager, TransactionDBManager

user_dbm = UserDBManager()
transaction_dbm = TransactionDBManager()


app = Flask(__name__)
api = Api(app)

class UserDatabase(Resource):
	def get(self):
		pass
	def delete(self):
		pass
	def put(self):
		pass
    def post(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name', type = str, required = True,
            help = 'No name provided', location = 'json')
        reqparser.add_argument('mobile_no', type = str, required = True,
            help = 'No mobile_no provided', location = 'json')
        reqparser.add_argument('email', type = str, required = True,
            help = 'No email provided', location = 'json')

        if self.add_user_to_db(reqparser.parse_args()):
        	return json.dumps({'result' : 'success'}), 201
        else:
        	return json.dumps({'result' : 'error'}), 666


    def add_user_to_db(self, data):
        return True

    def del_user_from_db(self, data):
    	return True

    def update_user(self, data):
    	return True

class Messenger(Resource):
	def get(self):
		pass
	def delete(self):
		pass
	def put(self):
		pass
	def post(self):
		reqparser = reqparse.RequestParser()

		reqparser.add_argument('number', type = str, required = True,
            help = 'No number provided', location = 'json')
        reqparser.add_argument('message', type = str, required = True,
            help = 'No message provided', location = 'json')

        message = reqparser['message']
        transaction_data = self.parse_message(message)

        user_id = user_dbm.find(args={'mobile_no' : reqparser['number']})

        transaction_dbm.process_transaction(args={'user_id' : user_id, 'transaction_data' : transaction_data})

    def parse_message(self, message):
    	pass


class TransactionsDB(Resource):
	def post(self):
		reqparser =reqparse.RequestParser()
		reqparser.add_argument('user_id', type = int, required = True,
			help = 'No user_id provided', location = 'json')
		reqparser.add_argument('transaction_data', type = str, required = True,
			help = 'No transaction_data provided', location = 'json')
		pass
	def get(self):
		pass
	def delete(self):
		pass
	def put(self):
		pass

	def process(self, transaction_data):
		pass


api.add_resource(UserDatabase, '/register')
api.add_resource(Messenger, '/message/receive')

if __name__ == '__main__':
    app.run(debug=True)