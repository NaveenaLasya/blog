import tornado.web

import pymongo
import motor

from tornado import gen



#extends get current user
class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		"""
		overrides get current user
		"""
		email=self.get_secure_cookie('email')
		if email:
			users_coll=self.application.db1.users
			user=users_coll.find_one({'email':email})
			if user:
				return user



#Handles /
class IndexHandler(BaseHandler):
	def get(self):
		"""
		display list of articles
		"""
		user = self.current_user
		if user:
			self.render('index.html',admin=True)
		else:
			self.render('index.html',admin=False)




