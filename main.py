from flask import Flask, render_template
from flask_socketio import SocketIO
from sys import getsizeof
from persistence.events import SimpleDBv2, Event
from queue import Queue
from threading import Thread
from persistence.canvas import Canvas, Pixel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
db = SimpleDBv2("events.db", "ab+")
# Init canvas from DB
canvas = Canvas(width=1600, height=800, db=db)
write_buffer = Queue(-1)

# TODO: Host this somewhere

class Consumer(Thread):
    def __init__(self, que: Queue, func):
        super(Consumer, self).__init__()
        self.buffer = que
        self.f = func

    def run(self):
        for elm in iter(self.buffer.get, None):
            self.f(elm)

Consumer(write_buffer, lambda line: db.addEvent(Event(line))).start()

# Send canvas down to to and render it
@app.route('/')
def renderCanvas():
    return render_template('canvas.html', async_mode=socketio.async_mode)

@socketio.on('connect')
def client_connected():
    socketio.emit('canvas', canvas.as_bytes())

@socketio.on('d')
def handle_draw(line):
    write_buffer.put(line)

    line_e = Event(line)
    print(line_e)
    start_pixel = Pixel(line_e.get_sx(), line_e.get_sy(), line_e.get_c_flag())
    end_pixel = Pixel(line_e.get_ex(), line_e.get_ey(), line_e.get_c_flag())
    canvas.set_line(start_pixel, end_pixel)

    socketio.emit('r', line, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)