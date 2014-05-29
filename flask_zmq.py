import zmq
from threading import Thread
from flask import current_app


class ZMQ(object):

	def __init__(self, app=None):
		self.context = zmq.Context()
		self.app = app
		self.router = {}
		self.subs = []
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		with app.app_context():
			app.config.setdefault('ZMQ_SOCKETTYPE', zmq.SUB)
			app.config.setdefault('ZMQ_CONNECT', "tcp://localhost:5560")

	def connect(self):
		with self.app.app_context():
			s = self.context.socket(current_app.config['ZMQ_SOCKETTYPE'])
			s.connect(current_app.config['ZMQ_CONNECT'])
		return s

	def subscribe(self, key):
		print self.connection
		def decorator(f):
			self.subs.append(key)
			self.router[key] = f
		return decorator

	@property
	def connection(self):
		if not hasattr(self, 'socket'):
			self.socket = self.connect()
		return self.socket

	def _process(self):
		self.context = zmq.Context()
		print self.connection
		for key in self.subs:
			self.connection.setsockopt(zmq.SUBSCRIBE, key)
		while True:
			key, payload = self.socket.recv_multipart()
			print "GOT A THING",key,payload
			if key in self.router:
				self.router[key](payload)


	def process(self):
		print "starting process"
		p = Thread(target=self._process)
		p.start()
