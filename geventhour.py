from gevent import monkey, sleep
monkey.patch_all()

from datetime import datetime
from flask import Flask, Response, request
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace

app = Flask(__name__)
app.debug = True


class Hour(BaseNamespace):
    def initialize(self):
        """Hello, feed the hour to this new guy"""
        self.spawn(self.ticker)

    def recv_disconnect(self):
        """Bye bye darling"""
        self.disconnect(silent=True)

    def ticker(self):
        """In a concurrent fashion, emit the date and time"""
        while True:
            self.emit('hour', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            sleep(0.5)


@app.route('/')
def index():
    """Default static HTML file"""
    return open('hour.html', 'r').read()


@app.route('/socket.io/<path:path>')
def socketio(path):
    """Handle the socketio requests"""
    socketio_manage(request.environ, {'/hour': Hour})
    return Response()


if __name__ == '__main__':
    server = SocketIOServer(
        ('', 5000), app, resource='socket.io', policy_server=True, policy_listener=('0.0.0.0', 10843)
    )
    server.serve_forever()
