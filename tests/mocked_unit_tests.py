import os, flask, flask_sqlalchemy, flask_socketio, random, datetime, pytz, re
import json, requests
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy.orm import relationship
from flask_socketio import SocketIO

import sys
sys.path.append("..")

import unittest
import unittest.mock as mock
from bot import chatBot
import main

KEY_INPUT = "input"
KEY_METHOD = "method"
KEY_EXPECTED = "expected"

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
#-----------------------------------------#
class UsrObj():
    def __init__(self, name, id):
        self.name = name
        self.id = id

class UsrTable():
    def __init__(self, name = "name", id = "email"):
        return
    
    def all(self):
        return [UsrObj("test name", "test email")]

class MsgObj():
    def __init__(self, text, name, time, user_id, image):
        self.text = text
        self.name = name
        self.time = time
        self.user_id = user_id
        self.image = image

class MsgTable():
    def __init__(self, text = "text", name = "name", time = "time", user_id = "email", image = "image"):
        return
    
    def all(self):
        return [MsgObj("test message", "test time", "test name", "test email", "test image")]
    
class SessionObj():
    def __init__(self):
        return
    def add(self, table):
        return
    def commit(self):
        return
    def query(self, table):
        return table
        
class db_test(unittest.TestCase):
    def setUp(self):
        self.success_user = [
            {
                KEY_INPUT: {
                    'name': 'name',
                    'email': 'email'
                },
                KEY_EXPECTED: None
            },
        ]
        self.success_message = [
            {
                KEY_INPUT: {
                    'message': 'hello',
                    'name': 'name',
                    'time': 'time',
                    'user_id': 'email',
                    'image':  'image'
                },
                KEY_EXPECTED: None
            },
        ]
    
    def test_add_new_message(self):
        for test in self.success_message:
            message = test[KEY_INPUT]['message']
            name = test[KEY_INPUT]['name']
            time = test[KEY_INPUT]['time']
            email = test[KEY_INPUT]['user_id']
            image = test[KEY_INPUT]['image']
            
            with mock.patch('main.db.session', SessionObj()):
                msg = MsgTable(message, name, time, email, image)
                
                response = SessionObj.add(self, msg)
                expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_commit_new_message(self):
        with mock.patch('main.db.session', SessionObj()):
            response = SessionObj.commit(self)
            expected = None
        self.assertEqual(response, expected)
        
    def test_query_message(self):
        for test in self.success_message:
            with mock.patch('main.db.session', SessionObj()):
                msgs = MsgTable()
                response = SessionObj.query(self, msgs)
                expected = msgs
            self.assertEqual(response, expected)
    
    def test_add_new_user(self):
        for test in self.success_user:
            name = test[KEY_INPUT]['name']
            email = test[KEY_INPUT]['email']
            
            with mock.patch('main.db.session', SessionObj()):
                usr = UsrObj(name, email)
                response = SessionObj.add(self, usr)
                expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_commit_new_user(self):
        with mock.patch('main.db.session', SessionObj()):
            response = SessionObj.commit(self)
            expected = None
        self.assertEqual(response, expected)
        
    def test_query_user(self):
        for test in self.success_user:
            with mock.patch('main.db.session', SessionObj()):
                usrs = UsrTable()
                response = SessionObj.query(self, usrs)
                expected = usrs
            self.assertEqual(response, expected)
#-----------------------------------------#
class mock_socket():
    def __init__(self):
        return
    def emit(self, channel, data):
        return
    
class socket_tests(unittest.TestCase):
    @mock.patch('main.db.session')
    def test_emit_all_messages(self, channel):
        msg = MsgObj(text = 'text', name = 'name', time = 'time', user_id = 'email', image = 'image')
        data = {
            'name': msg.name,
            'text': msg.text, 
            'time': msg.time,
            'image': msg.image,
            'email': msg.user_id
        }
        mock_socketio = mock_socket()
        with mock.patch('main.socketio', mock_socketio):
            result = mock_socketio.emit('send message', data)
        self.assertEqual(result, None)
    
    @mock.patch('main.db.session')
    def test_emit_all_users(self, channel):
        usrs = UsrObj(name = 'name', id = 'email')
        data = {
            'name': usrs.name,
            'email': usrs.id
        }
        mock_socketio = mock_socket()
        with mock.patch('main.socketio', mock_socketio):
            result = mock_socketio.emit('send user', data)
        self.assertEqual(result, None)
    
if __name__ == '__main__':
    unittest.main()    