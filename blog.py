import os.path
import pymongo
import motor

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pages
import profile

from tornado.options import define,options
define("port",default=8000,help="port addr",type=int)


MONGODB_URI = "mongodb://first:first@ds031872.mongolab.com:31872/first"

#handles the main class for configuration settings
class Application(tornado.web.Application):
	def __init__(self):
		handlers=[
		(r'/',pages.IndexHandler),
		(r'/register',profile.RegisterHandler),
		(r'/login',profile.LoginHandler),
		(r'/logout',profile.LogoutHandler)
				]
		settings=dict(
			template_path=os.path.join(os.path.dirname(__file__),"templates"),
			static_path=os.path.join(os.path.dirname(__file__),"static"),
			cookie_secret="Djsjdjikzxmnlkjuf&4nlDIOFSJ943qqjkj09",
			xsrf_cookies=True,
			debug=True,
			login_url='/login'
			)
		client1=pymongo.MongoClient(MONGODB_URI)
		client=motor.MotorClient(MONGODB_URI)
		self.db1=client1.first
		self.db=client.first
		tornado.web.Application.__init__(self,handlers,**settings)

if __name__=="__main__":
	tornado.options.parse_command_line()
	http_server=tornado.httpserver.HTTPServer(Application(),xheaders=True)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()