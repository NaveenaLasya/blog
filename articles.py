import tornado.web

import pymongo
import motor

import hashlib
from Crypto.Hash import SHA256

from tornado import gen


#extends get current user
class BaseHandler(tornado.web.RequestHandler):
	"""
		overrides get current user
	"""
	def get_current_user(self):
		email=self.get_secure_cookie('email')
		if email:
			users_coll=self.application.db1.users
			user=users_coll.find_one({'email':email})
			if user:
				return user

class AdminHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render('admin.html')
			
			

class CreateArticleHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render('createarticle.html')
	

	@tornado.web.asynchronous
	@gen.coroutine
	def post(self):
		articles_coll = self.application.db.articles
		articleauthor = self.get_argument("articleauthor") 
		articlename = self.get_argument("articlename")
		articledescription = self.get_argument("articledescription")
		article = dict()
		article['author'] = articleauthor
		article['name'] = articlename
		article['description'] = articledescription

		yield articles_coll.insert(article)
		self.render('createarticle.html',articlename=articlename,articledescription=articledescription,articleauthor=articleauthor)
		#self.write("u ve created an article")



class ReadArticleHandler(BaseHandler):
	@tornado.web.authenticated
	@tornado.web.asynchronous
	@gen.coroutine
	def get(self):
		articles_coll = self.application.db.articles
		articles=[]
		cursor = articles_coll.find()
		while (yield cursor.fetch_next):
			article = cursor.next_object()
			articles.append(article)
		self.render('readarticle.html',articles=articles)

		

	

	