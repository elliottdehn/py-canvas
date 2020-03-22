from flask import Flask, render_template
from flask_socketio import SocketIO, join_room
from sys import getsizeof

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def renderCanvas():
    return render_template('canvas.html', async_mode=socketio.async_mode)

@socketio.on('d')
def handle_draw(line):
    socketio.emit('r', line, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)