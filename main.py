from os.path import join, dirname
from dotenv import load_dotenv
import os, flask, flask_sqlalchemy, flask_socketio, random, datetime, pytz, re
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
    id = db.Column(db.String(75), primary_key=True)
    name = db.Column(db.String(50))
    messages = db.relationship('chatMessages', backref='users')
    
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def __repr__(self):
        return '<Username: %s\nEmail: %s>' % (self.name, self.id)
class chatMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.String(75), db.ForeignKey('users.id'))
    name = db.Column(db.String(120))
    time = db.Column(db.String(50))
    image = db.Column(db.String(150))
    
    def __init__(self, text, name, time, user_id, image):
        self.text = text
        self.name = name
        self.time = time
        self.user_id = user_id
        self.image = image
        
    def __repr__(self):
        return '<%s: %s \n%s \n%s\n%s>' % (self.name, self.text, self.time, self.user_id, self.image)
#-----------------------------------#
db.create_all()
db.session.commit()
active_users = []
numUsers = 0
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#-----------------------------------#
bot = bot.chatBot()
botID = "BimboBOT"
botImage = "https://www.internetandtechnologylaw.com/files/2019/06/iStock-872962368-chat-bots.jpg"
botDet = {
    'name': 'BimboBOT',
    'email': ' ',
    'imgUrl': botImage,
    'sid': botID
}
numUsers += 1
active_users.append(botDet)

print("\nChecking to see if BimboBOT exists...")
if db.session.query(Users.id).filter_by(name = "BimboBOT").scalar() is None:
    print("Created DB Entry for BimboBOT!\n")
    db.session.add(Users(name = "BimboBOT", id = botID))
    db.session.commit()
else:
    print("DB Entry for BimboBOT Exists!\n")
#-----------------------------------#
def emit_all_messages(channel):
    global all_messages
    all_messages = []
    for msg in db.session.query(chatMessages).all():
        all_messages.append({ 
            'name': msg.name, 
            'text': msg.text, 
            'time': msg.time,
            'image': msg.image,
            'email': msg.user_id
        })
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
    
    return full_name
def findUrl(string):
    regex = "(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url]
#-----------------------------------#
@socketio.on('new message')
def on_new_message(data):
    print("\nGot a new message: " + data['message'] + 
        "\nFrom User: " + data['name']
        )
    msg = data['message']
    username = data['name']
    image = data['imageUrl']
    user_id = data['user_id']
    date = datetime.datetime.now()
    time = str(datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%H:%M")) #NYC time
    time_str = (months[date.month - 1] + " " + str(date.day) + " \n@" + time)

    db.session.add(chatMessages(msg, username, time_str, user_id, image))
    db.session.commit()
    
    emit_all_messages('message received')
    
@socketio.on('new command')
def on_new_command(data):
    print("\nGot a new command: " + data['message'] + 
        "\nFrom User: " + data['name']
        )
    msg = data['message']
    username = data['name']
    image = data['imageUrl']
    user_id = data['user_id']
    date = datetime.datetime.now()
    time = str(datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%H:%M")) #NYC time
    time_str = (months[date.month - 1] + " " + str(date.day) + " \n@" + time)
    
    db.session.add(chatMessages(msg, username, time_str, user_id, image))
    db.session.commit()
    
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)
    
    bot_response = bot.command(msg)
    date = datetime.datetime.now()
    time = str(datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%H:%M")) #NYC time
    time_str = (months[date.month - 1] + " " + str(date.day) + " \n@" + time)
    
    db.session.add(chatMessages(bot_response, botID, time_str, botID, botImage))
    db.session.commit()

    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)

@socketio.on('new google')
def on_new_google(data):
    googleUsr = {
        'name': data['name'],
        'email': data['email'],
        'imgUrl': data['imgUrl'],
        'sid': request.sid
    }
    global numUsers 
    numUsers += 1
    print('\nNew Google User!' + 
            '\n-->Name: ' + googleUsr['name'] +
            '\n-->Email: ' + googleUsr['email'] +
            '\n-->Image: ' + googleUsr['imgUrl'] +
            '\nActive Users: ' + str(numUsers)
            )
    
    active_users.append(googleUsr)
    
    socketio.emit('set user', googleUsr)
    socketio.emit('active users', {
        'activeUsers': active_users,
        'numUsers': numUsers
    })
    if db.session.query(Users.id).filter_by(id = googleUsr['email']).scalar() is None:
        db.session.add(Users(name = googleUsr['name'], id = googleUsr['email']))
        db.session.commit()
        print("Created DB Entry for " + googleUsr['name'] + " with email " + googleUsr['email'])
    else:
        print("Welcome Back! " + googleUsr['name'])

    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)

@socketio.on('connect')
def on_connect():
    global numUsers
    print('\nSomeone Connected!\nActive Users: ' + str(numUsers))
    socketio.emit('active users', {
        'activeUsers': active_users,
        'numUsers': numUsers
    })
    emit_all_messages(MESSAGE_RECEIVED_CHANNEL)

@socketio.on('disconnect')
def on_disconnect():
    global numUsers
    for user in active_users:
        if user['sid'] == request.sid:
            active_users.remove(user)
            numUsers -= 1
            break
    print ('\nSomeone disconnected!\nActive Users: ' + str(numUsers))
    socketio.emit('active users', {
        'activeUsers': active_users,
        'numUsers': len(active_users)
    })

@app.route('/')
def index():
    socketio.emit('active users', {
        'activeUsers': active_users,
        'numUsers': numUsers
    })
    emit_all_messages(NEW_MESSAGE_CHANNEL)
    return flask.render_template('index.html')
    
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', IP),
        port=int(os.getenv('PORT', PORT)),
        debug=True
    )
