from flask import Flask, request, abort, redirect, render_template
from flask_login import LoginManager, login_user, current_user, UserMixin
from flask_socketio import SocketIO
import json

auth_code = {'12345':"Roco"}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'

login = LoginManager(app)
sio = SocketIO(app, cors_allowed_origins='*', manage_session=False, engineio_logger=True, logger=True)

@login.user_loader
def user_loader(id):
    return User(id)


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@app.route('/session/login', methods=['POST', 'GET'])
def login():
    print("Login")
    if request.method == 'POST':
        code = request.json.get('auth_code')
        if code not in auth_code:
            abort(401)
        else:
            login_user(User(auth_code.get(code)))
            print('Logged in', current_user.id)
            return json.dumps({"session_token":"sadaskldjsalkdjksajAASK565sd8sadasdsadsaj" })
    else:
        return json.dumps({"session_token":"" })


@sio.event
def connecting(environ):
    # Environ tiene toda la información del request del cliente.
    global auth_code

    print("Connecting")
    username = environ.get('HTTP_X_USERNAME')
    if not username:
        return False

    auth_code.update({username:request.sid})
    print(f"Users: {auth_code}")

    sio.emit('user_joined',json.dumps({username:request.sid}))

    print(request.sid,'Connected')

@sio.event
def echo(sid,data):
    username = data.get('HTTP_X_USERNAME')
    print(username)
    if not username:
        return False

    print(f"echo: {data}")
    sio.emit('echo',data,to=sid)

@sio.event
def disconnecting(sid,data):

    global users

    print(sid, 'Disconnecting')
    print(f"Environ {data}")
    username = data.get('HTTP_X_USERNAME')
    if not username:
        return False

    users.pop(username)

    print(f"Users: {username}")
    print(sid,'Disconnected')

    with sio.session(sid) as session:
        sio.emit('user_left', sid)

@sio.event
def chat(sid,data):
    username = data.get('from_user')
    to_username = data.get('to_user')
    print(f"Chat from: {username} to {to_username}")
    if not username and not to_username:
        return False

    user_sid = users.get(to_username)
    msg = data.get('msg')
    print(f'Say {msg} To user id: {user_sid}')
    sio.emit('chat',msg,to=user_sid)

if __name__ == '__main__':
    sio.run(app, debug=True,host='0.0.0.0',port='8000')