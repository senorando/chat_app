from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

PORT = 8080
IP = "0.0.0.0"

"""
TODO
"""

@app.route('/')
def hello():
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new number')
def on_new_number(data):
    print("Got an event for new number with data:", data)
    rand_number = data['number']
    socketio.emit('number received', {
        'number': rand_number
    })

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', IP),
        port=int(os.getenv('PORT', PORT)),
        debug=True
    )
