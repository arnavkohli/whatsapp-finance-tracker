
from twilio.rest import Client

class Messenger:

	def __init__(self, config):
		self._number = config['TwilioAPI']['NUMBER']
		self._client = Client(config['TwilioAPI']['ACCOUNT_SID'], config['TwilioAPI']['AUTH_TOKEN'])
		self._txn_types = config['TRANSACTION_TYPES']

	def send_message(self, to, body):
		message = self._client.messages.create(
                              body=body,
                              from_=self._number,
                              to=to
                          )
		print (message.sid)

	def is_clean(self, message):
		BAD = [
			'fk',
			'fuck',
			'fkk',
			'bitch',
			'pussy',
			'laude',
			'chut',
			'chyut',
			'chutiye',
			'gaand',
			'bhadwa',
			'bc',
			'mc',
			'bhenchod',
			'madarchod',
			'maa',
		]
		return not any([m.lower() in str(BAD) for m in message])

	def parse_message(self, message):
		message = message.split(' ')
		message = [m for m in message if m != None and m.strip() != '']

		if message[0].lower() == 'bugreport':
			if self.is_clean(message[1:]):
				print (f"######## BUGREPORT ########: {' '.join(message[1:])}")
				return {"cmd" : "send_thanks"}
			else:
				return {"cmd" : "send_gaali"}

		elif len(message) == 1:
			if message[0].lower() == 'all':
				return {"cmd" : "all"}
			elif message[0].lower() == 'summary':
				return {"cmd" : "summary"}
			elif message[0].lower() == 'help':
				return {"cmd" : "help"}

		# delete cmd
		elif len(message) == 2:
			del_cmd, txn_id = message
			return {"cmd" : "delete", "data" : {"id" : txn_id}}

		# add txn command
		elif len(message) == 3:

			txn_type, amount, name = message
			txn_type = txn_type.lower()
			amount = int(amount)

			if txn_type not in self._txn_types:
				return Exception('invalid transaction type')

			return {"cmd" : "add" , "data" : {"type" : txn_type, "amount" : amount, "person_name" : name}}

		# update txn command
		elif len(message) == 5:

			update_cmd, txn_id, txn_type, amount, name = message
			txn_type = txn_type.lower()
			amount = int(amount)

			if txn_type not in self._txn_types:
				return Exception('invalid transaction type')

			return {"cmd" : "update" , "data" : {"type" : txn_type, "amount" : amount, "person_name" : name, "id" : txn_id}}

		else:
			raise Exception('invalid command')