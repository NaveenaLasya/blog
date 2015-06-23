import os.path
import pymongo
import motor

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from datetime import date

import pages
import profile
import articles

from tornado.options import define,options
define("port",default=8000,help="port addr",type=int)


MONGODB_URI = "mongodb://first:first@ds031872.mongolab.com:31872/first"

#handles the main class for configuration settings
class Application(tornado.web.Application):
	def __init__(self):
		handlers=[
		(r'/',pages.IndexHandler),
		(r'/arts',pages.artsHandler),
		(r'/register',profile.RegisterHandler),
		(r'/login',profile.LoginHandler),
		(r'/admin',articles.AdminHandler),
		(r'/createarticle',articles.CreateArticleHandler),
		(r'/android_login',profile.AndroidLoginHandler),
		(r'/api_login',profile.ApiLoginHandler),
		(r'/readarticle',articles.ReadArticleHandler),
		(r'/api',articles.ApiArticleHandler),
		(r'/logout',profile.LogoutHandler),
		(r'/.*',profile.ErrorHandler)
				]
		settings=dict(
			template_path=os.path.join(os.path.dirname(__file__),"templates"),
			static_path=os.path.join(os.path.dirname(__file__),"static"),
			assets_path=os.path.join(os.path.dirname(__file__),"assets"),
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