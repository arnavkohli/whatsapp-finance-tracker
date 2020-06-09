import json
from datetime import datetime
import random



class Manager:

	def __init__(self, config):
		self._users_fp = config['USERS_FILE_PATH']
		try:
			self._users = json.loads(open(self._users_fp, 'r').read())
		except:
			self._users = []

		self._transactions_fp = config['TRANSACTIONS_FILE_PATH']
		try:
			self._transactions = json.loads(open(self._transactions_fp, 'r').read())
		except:
			self._transactions = []

		self.TRANSACTION_TYPES = config['TRANSACTION_TYPES']
		print (type(self.TRANSACTION_TYPES))
		print (self.TRANSACTION_TYPES)

	def txn_types(self):
		return self.TRANSACTION_TYPES

	@property
	def users(self):
		return self._users
	
	@property
	def transactions(self):
		return self._transactions

	def get_user_by_number(self, number):
		for user in self._users:
			if str(user['number']) == str(number):
				return user
		return None

	def summary(self, eyed):
		by_type = {}
		by_person_name = {}

		txns = self.get_user_transactions(eyed, types='all')

		for txn in txns:
			txn_type = txn['type']
			txn_entity = txn['person_name']
			txn_amount = float(txn['amount'])

			if txn_type not in by_type:
				by_type[txn_type] = txn_amount
			else:
				by_type[txn_type] += txn_amount

			if txn_entity not in by_person_name:
				if txn_type == 'withdraw':
					by_person_name[txn_entity] = txn_amount
			else:
				if txn_type == 'withdraw':
					by_person_name[txn_entity] += txn_amount

		text = f'*Summary for UserID: {eyed}*' + '\n'
		text += '*Type Wise*\n'

		curr_delta = 0
		pending_delta = 0

		for t in by_type:
			text += f'```{t}``` : _{int(by_type[t])}/-_\n'
			if t == 'deposit':
				curr_delta += int(by_type[t])
			elif t == 'withdraw':
				curr_delta -= int(by_type[t])
			elif t == 'lent':
				pending_delta += int(by_type[t])
			elif t == 'owe':
				pending_delta -= int(by_type[t])
		text += '*Detailed Expenditure*\n'
		for pname in by_person_name:
			text += f'```{pname}``` : _{by_person_name[pname]}/-_\n'

		text += '*Overview*\n'
		text += f'```Current Delta```: _{curr_delta}_\n'
		text += f'```(Lent/Owe) Delta```: _{pending_delta}_\n'
		text += f'```Net Delta```: _{curr_delta + pending_delta}_\n'

		return text

	def get_user_transactions(self, eyed, types):
		result = []
		for transaction in self._transactions:
			if str(transaction['user_id']) == str(eyed) and (types == 'all' or transaction['type'] in types):
				result.append(transaction)
		return result
		# return self.clean_user_transactions(result,)

	def clean_user_transactions(self, eyed, types):
		data = self.get_user_transactions(eyed, types)
		line = '-'*15
		text = line + '\n' + f'Transactions for UserID: {eyed}' + '\n' + line + '\n'
		for txn in data:
			for txn_var in [col for col in txn if col not in ['lastModified', 'user_id', 'createdAt']]:
				text += f'{txn_var}: {txn[txn_var]}\n'
			text += line + '\n'
		return text


	def get_transaction_index(self, eyed):
		for index, transaction in enumerate(self._transactions):
			if str(transaction['id']) == str(eyed):
				return index
		return None

	def get_user_index(self, eyed):
		for index, user in enumerate(self._users):
			if str(user['id']) == str(eyed):
				return index
		return None

	def get_user(self, eyed):
		try:
			return self._users[self.get_user_index(eyed)]
		except:
			return {"error" : "no such user found"}

	def get_transaction(self, eyed):
		try:
			return self._transactions[self.get_transaction_index(eyed)]
		except:
			return {"error" : "no such transaction found"}

	def add_user(self, user):
		user['id'] = random.randint(100000, 999999)
		user['createdAt'] = datetime.now().__str__()
		user['lastModified'] = user['createdAt']
		if self.is_valid_user(user):
			self._users.append(user)
			self.refresh_users()
		else:
			raise Exception('not valid user')

	def add_transaction(self, transaction):
		transaction['id'] = random.randint(100000, 999999)
		transaction['createdAt'] = datetime.now().__str__()
		transaction['lastModified'] = transaction['createdAt']
		transaction['amount'] = float(transaction['amount'])
		if self.is_valid_transaction(transaction):
			self._transactions.append(transaction)
			self.refresh_transactions()
		else:
			raise Exception('not valid transaction')

	def update_user(self, new_user):
		old_user = self._users[self.get_user_index(new_user['id'])]
		new_user['createdAt'] = old_user['createdAt']
		new_user['lastModified'] = datetime.now().__str__()
		if self.is_valid_user(new_user):
			self._users[self.get_user_index(new_user['id'])] = new_user
			self.refresh_users()
		else:
			raise Exception('not valid user')

	def update_transaction(self, new_txn):
		old_txn = self._transactions[self.get_transaction_index(new_txn['id'])]
		new_txn['id'] = old_txn['id']
		new_txn['createdAt'] = old_txn['createdAt']
		new_txn['lastModified'] = datetime.now().__str__()
		if self.is_valid_transaction(new_txn):
			self._transactions[self.get_transaction_index(new_txn['id'])] = new_txn
			self.refresh_transactions()
		else:
			raise Exception('not valid transaction')

	def delete_user(self, eyed):
		self._users.pop(self.get_user_index(eyed))
		self.refresh_users()

	def delete_transaction(self, eyed):
		self._transactions.pop(self.get_transaction_index(eyed))
		self.refresh_transactions()


	def is_valid_user(self, data):
		cols = [
			'id',
			'name',
			'password',
			'number',
			'email',
			'createdAt',
			'lastModified'
		]
		col_count = len(cols)

		return all([col in data for col in cols]) and len(data) == col_count


	def is_valid_transaction(self, data):
		cols = [
			'id',
			'user_id',
			'type',
			'amount',
			'person_name',
			'createdAt',
			'lastModified'
		]
		col_count = len(cols)

		if all([col in data for col in cols]) and len(data) == col_count:
			transaction_type = data['type']
			if transaction_type.lower() in self.TRANSACTION_TYPES:
				return True
		return False

	def refresh_users(self):
		with open(self._users_fp, 'w') as f:
			json.dump(self.users, f, indent=4)

	def refresh_transactions(self):
		with open(self._transactions_fp, 'w') as f:
			json.dump(self.transactions, f, indent=4)

	def master_refresh(self):
		self.refresh_users()
		self.refresh_transactions()

	def get_users(self):
		try:
			with open(self._users_fp, 'r') as f:
				return json.loads(f.read())
		except:
			return []

	def get_transactions(self):
		try:
			with open(self._transactions_fp, 'r') as f:
				return json.loads(f.read())
		except:
			return []