import tornado.web

import pymongo
import motor
import time
import datetime
import json
import pages


import pages

import hashlib
from Crypto.Hash import SHA256
# from httpclient import HttpRequest
from tornado import gen
from bson import json_util
from time import strftime
import jwt

import memcache
mc = memcache.Client(['0.0.0.0:11211'],debug=1)


MONGODB_URI = "mongodb://first:first@ds031872.mongolab.com:31872/first"



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
		# print "success"
		# token= self.request.headers.get('version','')
		# #token =self.get_argument("logintoken")
		# print token 
		#user, _, pwd= base64.decodestring(token).partition(':')
		# email =jwt.decode(token, 'cookie_secret', algorithms=['HS256'])
		# if email:
		# 	users_coll=self.application.db1.users
		# 	user=users_coll.find_one({'email':email})
		# 	if user:
		# 		return user

	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin","*")

class AdminHandler(BaseHandler):
	"""
		Welcome page for admin
	"""
	@tornado.web.authenticated
	def get(self):
		self.render('admin.html')
			
			

class CreateArticleHandler(BaseHandler):
	"""
		For creating an article
	"""
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
		article['time'] = time.time()
		article['date'] = strftime("%d/%m/%Y")
		yield articles_coll.insert(article)
		key= 'blog'
 		d=self.application.db1
 		a=pages.ar()
 		up=True
 		final_articles = a.fdarticles(d,key,up)
		self.render('createarticle.html')
		


class ReadArticleHandler(BaseHandler):
	"""
		Reading articles
	"""
	@tornado.web.authenticated
	@tornado.web.asynchronous
	@gen.coroutine
	def get(self):
		articles_coll = self.application.db.articles
		articles={}
		cursor = articles_coll.find()
		while (yield cursor.fetch_next):
			article = cursor.next_object()
			articles[article['name']]=article
		self.write(json.dumps(articles,default=json_util.default))

class ApiArticleHandler(tornado.web.RequestHandler):
	update = False
	
	@tornado.web.asynchronous
 	@gen.coroutine
 	def get(self):
 		#user_details=dict()
		#users_coll = self.application.db.users 
		logintoken=self.get_argument("logintoken")
		#currentuser=yield users_coll.find_one({'logintok':logintoken})
		# if currentuser: 
		# 	loginpassword=SHA256.new(loginpassword).hexdigest()
		# 	if loginpassword==currentuser['password']:
		# 		currentusername=currentuser['name']
		# 		self.set_secure_cookie("email",loginemail)
		# 		user_details=dict()
		# 		user_details['token'] = currentuser['token']
		# 		user_details['email'] = currentuser['email']
		# 		user_details['Success'] = "1"
		# 	else:
		# 		user_details['message'] = "username"
		# 		user_details['Success'] = "False"
		# 	self.write(json.loads(json_util.dumps(user_details)))	
		# else:
		# 	self.write("please register")
		if logintoken:
			# re = self.request('https://localhost:8000/api?logintoken="DSf"')
			# print re
			header= self.request.headers.get('Accept-Language')

			print "failed"
			token={"header":header}
			print header
			self.write(token)
	 		key= 'blog'
	 		# h=self.get_default_headers(self.get_header("Access-Control-Allow-Origin"))
	 		# print h

	 		# d=self.application.db1
	 		# a=pages.ar()
	 		# final_articles = a.fdarticles(d,key,ApiArticleHandler.update)
	 		# self.write(tornado.escape.json_encode(final_articles))
	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin","*")
		self.set_header("Access-Control-Allow-Headers","*")
		self.set_header("Access-Control-Allow-Methods","GET,OPTIONS")








# class HeaderHandler(tornado.httpclient.HTTPRequest):
# 	def get(self):
# 		data = HttpRequest.META
# 		self.write(data)
	

	