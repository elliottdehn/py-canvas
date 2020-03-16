from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def renderCanvas():
    return render_template('canvas.html')

@socketio.on('draw')
def handle_draw_event(event):
    print('received event: ' + event)

if __name__ == '__main__':
    socketio.run(app)