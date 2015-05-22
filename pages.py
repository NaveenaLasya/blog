import tornado.web

import pymongo
import motor

from tornado import gen

#extends get current user
class BaseHandler(tornado.web.RequestHandler):
	#overrides get current user
	def get_current_user(self):
		email=self.get_secure_cookie('email')
		if email:
			users_coll=self.application.db1.users
			user=users_coll.find_one({'email':email})
			if user:
				return user


#Handles / 
class IndexHandler(tornado.web.RequestHandler):
	#display list of articles
	def get(self):
		self.write("no articles sry")




