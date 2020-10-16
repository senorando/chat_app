from os.path import join, dirname
from dotenv import load_dotenv
import os, flask, flask_sqlalchemy, flask_socketio, random
from flask import session, redirect, url_for, request
from markupsafe import escape
from sqlalchemy.orm import relationship

from flask_socketio import SocketIO, join_room, leave_room;

NEW_MESSAGE_CHANNEL = 'new message'
MESSAGE_RECEIVED_CHANNEL = 'message received'
USER_RECEIVED_CHANNEL = 'users received'

app = flask.Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

PORT = 8080
IP = "0.0.0.0"

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app
#-----------------------------------#
class Users(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(30))
    messages = db.relationship('chatMessages', backref='users')
    
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def __repr__(self):
        return '<Username: %s>' % self.name
class chatMessages(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'))
    
    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id
        
    def __repr__(self):
        return '<Message: %s>' % self.text
#-----------------------------------#
db.create_all()
db.session.commit()
active_users = []
#-----------------------------------#
def emit_all_users(channel):
    all_users = [ \
        db_message.name for db_message \
        in db.session.query(Users).all()]
        
    socketio.emit(channel, {
        'allUsers': all_users
    })
def emit_all_messages(channel):
    all_messages = [ \
        db_message.text for db_message \
        in db.session.query(chatMessages).all()]
    socketio.emit(channel, {
        'allMessages': all_messages
    })
def genUserName():
    guest_n1 = ["strange", "smelly", "hungry", "angry", "rich", "annoying", "goofy", "lonely", "lazy", "edible"];
    guest_n2 = ["Dinosaur", "Cow", "Donkey", "Hippo", "Person", "Tortilla", "Dog", "Cat", "Turtle", "Sloth"];
    rand = random.randint(0, 50)
    rand_n1 = random.randint(0, len(guest_n1) - 1)
    rand_n2 = random.randint(0, len(guest_n2) - 1)
    full_name = (guest_n1[rand_n1] + guest_n2[rand_n2] + str(rand))
    
    return full_name;
#-----------------------------------#
 
@socketio.on('new message')
def on_new_message(data):
    print("\nGot a new message: " + data[0]['message'] + 
        "\nFrom User: " + Users.query.filter_by(id = data[1]['user_id']).first().name
        )
    message = data[0]['message']
    username = Users.query.filter_by(id = data[1]['user_id']).first().name
    db.session.add(chatMessages((username + ": " + message), data[1]['user_id']))
    db.session.commit()
    
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)
    
@socketio.on('connect')
def on_connect():
    user = genUserName()
    print ('\nSomeone connected!' + '\nUsername: ' + user + '\nSID: ' + request.sid + "\n")
    active_users.append(user)
    socketio.emit('set user', {
        'name': user,
        'user_id': request.sid
    })
    
    socketio.emit('active users', {
        'activeUsers': active_users
    })
    db.session.add(Users(name = user, id = request.sid))
    db.session.commit()
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)
    emit_all_users(USER_RECEIVED_CHANNEL)
    
    
@socketio.on('disconnect')
def on_disconnect():
    active_users.remove(Users.query.filter_by(id = request.sid).first().name)
    
    socketio.emit('active users', {
        'activeUsers': active_users
    })
    print ('\nSomeone disconnected!')

@app.route('/')
def index():
    emit_all_users('connect')
    emit_all_messages(NEW_MESSAGE_CHANNEL)
    return flask.render_template('index.html')
    
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', IP),
        port=int(os.getenv('PORT', PORT)),
        debug=True
    )
