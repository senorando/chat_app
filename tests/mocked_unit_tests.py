import json,requests,random,os
from os.path import join, dirname
from dotenv import load_dotenv

import sys
sys.path.append("..")

import unittest
import unittest.mock as mock
from bot import chatBot
#from models import Users, chatMessages
# import main

class bot_tests(unittest.TestCase):
    headers = {'Content-Type': 'application/json'}
    input = "The quick brown fox jumped over the lazy dog"
    
    def test_request_success(self):
        api_url = 'https://api.funtranslations.com/translate/yoda.json?text={}'.format(self.input)
        with mock.patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            response = requests.get(api_url, headers = self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_request_failure(self):
        api_url = 'https://api.funtranslations.com/translate/yoda.json?text={}'.format(self.input)
        with mock.patch('requests.get') as mock_get:
            mock_get.return_value.status_code = None
            response = requests.get(api_url, headers = self.headers)
        self.assertEqual(response.status_code, None)

class db_tests(unittest.TestCase):
    
    def mockdb(self, app):
        x = 1
    
class socket_tests(unittest.TestCase):
    x = 1
    
if __name__ == '__main__':
    unittest.main()    