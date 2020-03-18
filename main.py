from flask import Flask, render_template
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def renderCanvas():
    return render_template('canvas.html', async_mode=socketio.async_mode)

@socketio.on('drawLine')
def handle_draw(line):
    print(line)
    socketio.emit('renderLine', line, room='connected')

@socketio.on('connect')
def handle_connect():
    join_room('connected')


if __name__ == '__main__':
    socketio.run(app)