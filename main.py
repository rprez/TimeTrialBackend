import socketio
import random
import json

print('Start Socket Server')
sio = socketio.Server(cors_allowed_origins='*')

app = socketio.WSGIApp(sio,static_files={
    '/': './public/'
})

client_count = 0
a_count = 0
b_count = 0

users = {}

def task(sid):
    sio.sleep(5)
    #sio.emit('mult', {'numbers': [3,4]},callback=cb)
    #La función call lo que hace es lo mismo que el emit y el callback
    result = sio.call('mult', {'numbers': [3, 4]},to=sid)
    #sio.emit()
    #sio.send() # Es lo mismo que emit pero con el event "message"
    print(result)

@sio.event
def connecting(sid,environ):
    # Environ tiene toda la información del request del cliente.
    global users

    print("Connecting")
    username = environ.get('HTTP_X_USERNAME')
    if not username:
        return False

    with sio.session(sid) as session:
        users.update({username:sid})
        print(f"Users: {users}")

    sio.emit('user_joined',json.dumps({username:sid}))

    print(sid,'Connected')


@sio.event
def aux_conectar(sid,environ):
    # Environ tiene toda la información del request del cliente.
    global client_count
    global a_count
    global b_count

    print("Conectando")
    username = environ.get('HTTP_X_USERNAME')
    if not username:
        return False

    with sio.session(sid) as session:
        #users = session.get('users',{})
        users.update({username:sid})
        print(f"Users: {users}")
        #session['users'] = users

    sio.emit('user_joined',json.dumps({username:sid}))

    client_count += 1
    print(sid,'connected')
    #sio.start_background_task(task,sid)

    sio.emit('client_count',client_count)
    if random.random() > 0.5:
        print("ROOM A")
        sio.enter_room(sid,'room_a')
        a_count += 1
        sio.emit('room_count', a_count,to='room_a')
    else:
        print("ROOM B")
        sio.enter_room(sid, 'room_b')
        b_count += 1
        sio.emit('room_count', b_count,to='room_b')

@sio.event
def echo(sid,data):
    username = data.get('HTTP_X_USERNAME')
    print(username)
    if not username:
        return False

    print(f"echo: {data}")
    sio.emit('echo',data,to=sid)


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
def desconectar(sid,environ):
    global client_count
    global a_count
    global b_count
    client_count -= 1

    print(sid,'DESCONECTAR')
    username = environ.get('HTTP_X_USERNAME')
    if not username:
        return False

    sio.emit('client_count',client_count)
    if 'room_a' in sio.rooms(sid):
        a_count -= 1
        sio.emit('room_count', a_count, to='room_a')
    else:
        b_count -= 1
        sio.emit('room_count', b_count, to='room_b')

    with sio.session(sid) as session:
        #print(f"echo: {session}")
        #users = session.get('users',{})
        user = users.pop(username)
        sio.emit('user_left', user)
    print(f"Usuario desconectado: {username}")

@sio.event
def sum(sid,data):
    result = data['numbers'][0] + data['numbers'][1]
    #sio.emit('sum_result', {'result':result},to=sid)
    #Call Back
    return {"result": result }


