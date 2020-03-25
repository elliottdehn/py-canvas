from flask import Flask, render_template
from flask_socketio import SocketIO, join_room
from sys import getsizeof
from persistence import SimpleDBv2, Event
from queue import Queue
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
db = SimpleDBv2()

write_buffer = Queue(-1)
class Consumer(Thread):
    def __init__(self, que: Queue, func):
        super(Consumer, self).__init__()
        self.buffer = que
        self.f = func

    def run(self):
        for elm in iter(self.buffer.get, None):
            self.f(elm)

Consumer(write_buffer, lambda line: db.addEvent(Event(line))).start()

@app.route('/')
def renderCanvas():
    return render_template('canvas.html', async_mode=socketio.async_mode)

@socketio.on('d')
def handle_draw(line):
    write_buffer.put(line)
    socketio.emit('r', line, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)