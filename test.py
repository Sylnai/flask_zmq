import json
from flask import Flask
from flask.ext.zmq import ZMQ
app = Flask(__name__)
zmq = ZMQ(app)

alerts = {}

@zmq.subscribe("web")
def pinggotten(ping):
	ping = json.loads(ping)
	alerts[ping["user"]] = ping

@app.route('/')
def hello_world():
	return 'Hello World!'

if __name__ == '__main__':
	with app.app_context():
		zmq.process()
	app.run(host='0.0.0.0', debug=True)
