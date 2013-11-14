
from gevent import monkey, sleep, spawn
monkey.patch_all()

from gevent.event import AsyncResult

from datetime import datetime
from flask import Flask, Response, request
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace

app = Flask(__name__)
app.debug = True

last_tweet = AsyncResult()


class HourAndTweet(BaseNamespace):
    def initialize(self):
        """Hello, feed the hour and tweets to this new guy"""
        self.spawn(self.ticker)

    def recv_disconnect(self):
        """Bye bye darling"""
        self.disconnect(silent=True)

    def ticker(self):
        """In a concurrent fashion, emit the date and time and new tweet"""
        while True:
            self.emit('hour', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            try:
                tweet = last_tweet.get(block=False)
            except:
                pass
            else:
                self.emit('tweet', tweet)
            sleep(0.1)


@app.route('/')
def index():
    """Default static HTML file"""
    return open('tweets.html', 'r').read()


@app.route('/socket.io/<path:path>')
def socketio(path):
    """Handle the socketio requests"""
    socketio_manage(request.environ, {'/tweet': HourAndTweet})
    return Response()


from twython import TwythonStreamer

APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
FILTER = 'python'
options = (APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


class TweetStreamer(TwythonStreamer):
    def __init__(self, *options):
        TwythonStreamer.__init__(self, *options)
        self.run()

    def on_success(self, data):
        if 'text' in data:
            last_tweet.set(data['text'].encode('utf-8'))

    def on_error(self, status_code, data):
        print('TweetStreamer error {}'.format(status_code))
        self.disconnect()

    def run(self):
        self.statuses.filter(track=FILTER)


if __name__ == '__main__':
    stream = spawn(TweetStreamer, *options)

    server = SocketIOServer(
        ('', 5000), app, resource='socket.io', policy_server=True, policy_listener=('0.0.0.0', 10843)
    )
    stream.link(server.stop)
    server.serve_forever()
