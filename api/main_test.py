import unittest
import requests

base = 'http://127.0.0.1:8080/'


class TestSum(unittest.TestCase):

    def test_user_created(self):
    	url = base + 'user'
    	data = {
    		'name' : 'huhlhlhlhl',
    		'password' : 'password',
    		'email' : 'asa@gmail.com',
    		'number' : '92032302'
    	}
    	headers = {"Content-Type" : "application/json"}
    	response = requests.post(url=url, json=data, headers=headers)
    	self.assertEqual(response.status_code, 200, "Should receive 200")

    def test_user_updated(self):
    	url = base + 'user'
    	data = {
    		'id' : 468265,
    		'name' : 'Test2',
    		'password' : 'password',
    		'email' : 'asa@gmail.com',
    		'number' : '92032302'
    	}
    	headers = {"Content-Type" : "application/json"}
    	response = requests.put(url=url, json=data, headers=headers)
    	self.assertEqual(response.status_code, 200, "Should receive 200")

    # def test_user_deleted(self):
    # 	url = base + 'user' + '/999361'
    # 	headers = {"Content-Type" : "application/json"}
    # 	response = requests.delete(url=url, headers=headers)
    # 	self.assertEqual(response.status_code, 200, "Should receive 200")
    	# self.assertEqual(response.json()['result'], 'success', "Should receive 200")

    # def test_sum_tuple(self):
    #     self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()