//Aqui se puede espicificar el origen de los socket de conexión.
//Estoy creando una conexión nueva.
const sio = io({
    transportOptions: {
        polling: {
            extraHeaders: {
                'X-Username': window.location.hash.substring(1)
            }
        }
    }
});

sio.on('connect', () => {
    console.log('Connected');

    //La forma de envíar un mensaje (evento ) es con sio.emit(nombre,objeto)
    sio.emit('sum', {numbers: [1,2]}, (result) => {
        console.log(result);
    })

});

sio.on('connect_error', (e) => {
    console.log(e.message)
});

sio.on('disconnect', () => {
    console.log('Disconnect');
});

//sio.on('sum_result', (data) => {
//    console.log(data);
//});

sio.on('mult', (data, callback) => {
    console.log(data);
    const result = data.numbers[0] * data.numbers[1];
    callback(result);
});

sio.on('client_count', (count) => {
    console.log('There are ' + count + ' connected clients.')
})

sio.on('room_count', (count) => {
    console.log('There are ' + count + ' clients in my room.')
})

sio.on('user_joined', (username) => {
    console.log('User ' + username + ' has joined')
})

sio.on('user_left', (username) => {
    console.log('User ' + username + ' has left')
})