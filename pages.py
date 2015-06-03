import tornado.web

import pymongo
import motor
import time
import json

from tornado import gen
from bson import json_util



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

	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin","*")



#Handles /
class IndexHandler(BaseHandler):
	@tornado.web.asynchronous
	@gen.coroutine
	def get(self):
		"""
		display list of articles
		"""
		#user = self.current_user
		#if user:
		#	self.render('admin.html',admin=True)
		#else:
		articles_coll = self.application.db.articles
		articles={}
		cursor = articles_coll.find()
		i=1
		while (yield cursor.fetch_next):
			article = cursor.next_object()
			art_obj = dict()
			art_obj['title']=article['name']
			art_obj['body']=article['description']
			art_obj['published']=article['time']
			art_obj['author']=article['author']
			articles[i] = art_obj
			i+=1
		
		self.write(articles)
			#self.render('index.html',admin=False)




