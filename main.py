from os.path import join, dirname
from dotenv import load_dotenv
import os, flask, flask_sqlalchemy, flask_socketio, random
from flask import session, redirect, url_for, request
from markupsafe import escape
from sqlalchemy.orm import relationship
from flask_socketio import SocketIO, join_room, leave_room
import bot

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
    name = db.Column(db.String(50))
    
    def __init__(self, text, name):
        self.text = text
        self.name = name
        #self.name = Users.query.filter_by(id = self.user_id).first().name
        
    def __repr__(self):
        return '<%s: %s>' % (self.name, self.text)
#-----------------------------------#
db.create_all()
db.session.commit()
active_users = []
numUsers = 0
#-----------------------------------#
bot = bot.chatBot()
botID = "BimboBOT"
print("\nChecking to see if BimboBOT exists...")
if db.session.query(Users.id).filter_by(name = "BimboBOT").scalar() is None:
    print("Created DB Entry for BimboBOT!\n")
    db.session.add(Users(name = "BimboBOT", id = botID))
    db.session.commit()
else:
    print("DB Entry for BimboBOT Exists!\n")
#-----------------------------------#
def emit_all_users(channel):
    all_users = [ \
        db_message.name for db_message \
        in db.session.query(Users).all()]
        
    socketio.emit(channel, {
        'allUsers': all_users
    })
def emit_all_messages(channel):
    global all_messages
    all_messages = []
    for msg in db.session.query(chatMessages).all():
        all_messages.append({ 'name': msg.name, 'text': msg.text })
    socketio.emit(channel, {
        'allMessages': all_messages
    })
def genUserName():
    guest_n1 = ["strange", "smelly", "hungry", "angry", "rich", "annoying", "goofy", "lonely", "lazy", "edible", "adorable", "homely", "impossible", "disturbed", "agreeable", "shy", "dull", "spotless", "jolly", "jittery", "annoying", "doubtful", "dizzy", "itchy", "inquisitive", "splendid", "lively", "breakable", "lucky", "super", "tender", "troubled", "muddy", "fancy", "cautious", "fragile", "mushy", "tasty", "uptight", "obnoxious", "glamorous", "clumsy", "concerned", "odd", "clever", "grieving", "grotesque", "grumpy", "poised", "plain", "wild", "witty", "prickly", "wicked", "hilarious", "defeated", "puzzled", "boorish", "irksome", "obtuse"];
    guest_n2 = ["Dinosaur", "Turtle", "Cow", "Donkey", "Hippo", "Person", "Tortilla", "Dog", "Cat", "Turtle", "Sloth", "Sock", "Monkey", "Baby", "Hero", "Peacock", "Boar", "Caterpillar", "Clam", "Sardine", "Walrus", "Bee", "Iguana", "Hamster", "Aardvark", "Alpaca", "Barracuda", "Baboon", "Camel", "Armadillo", "Chicken", "Dragon", "Eagle", "Elephant", "Ferret", "Flamingo", "Fox", "Panda", "Giraffe", "Hawk", "Gazelle", "Hog", "Jellyfish", "Lemur", "Llama", "Narwhal", "Otter", "Penguin", "Pelican", "Raccoon", "Sheep", "Snail", "Turkey", "Weasel"];
    rand = random.randint(0, 50)
    rand_n1 = random.randint(0, len(guest_n1) - 1)
    rand_n2 = random.randint(0, len(guest_n2) - 1)
    full_name = (guest_n1[rand_n1] + "_" + guest_n2[rand_n2])
    
    return full_name;
#-----------------------------------#
@socketio.on('new message')
def on_new_message(data):
    print("\nGot a new message: " + data['message'] + 
        "\nFrom User: " + data['name']
        )
    msg = data['message']
    username = data['name']
        
    db.session.add(chatMessages(msg, username))
    db.session.commit()
    
    emit_all_messages('message received')
    
@socketio.on('new command')
def on_new_command(data):
    print("\nGot a new command: " + data['message'] + 
        "\nFrom User: " + data['name']
        )
    msg = data['message']
    username = data['name']
        
    db.session.add(chatMessages(msg, username))
    db.session.commit()
    
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)
    
    bot_response = bot.command(msg)
    
    db.session.add(chatMessages(bot_response, botID))
    db.session.commit()
    
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)
    
@socketio.on('connect')
def on_connect():
    user = genUserName()
    print ('\nSomeone connected!' + '\nUsername: ' + user + '\nSID: ' + request.sid + "\n")
    global numUsers
    numUsers += 1
    active_users.append(user)
    socketio.emit('set user', {
        'name': user,
        'user_id': request.sid
    })
    socketio.emit('active users', {
        'activeUsers': active_users,
        'numUsers': numUsers
    })
    db.session.add(Users(name = user, id = request.sid))
    db.session.commit()
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)
    emit_all_users(USER_RECEIVED_CHANNEL)
    
@socketio.on('disconnect')
def on_disconnect():
    active_users.remove(Users.query.filter_by(id = request.sid).first().name)
    global numUsers 
    numUsers -= 1
    socketio.emit('active users', {
        'activeUsers': active_users,
        'numUsers': numUsers
        
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
