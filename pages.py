import tornado.web

import pymongo
import motor
import time
import json
import logging

from tornado import gen
from bson import json_util

import memcache
mc = memcache.Client(['0.0.0.0:11211'],debug=1)




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


def get_articles():

	MONGODB_URI = "mongodb://first:first@ds031872.mongolab.com:31872/first"
	client1=pymongo.MongoClient(MONGODB_URI)
	client=motor.MotorClient(MONGODB_URI)
	db1=client1.first
	db=client.first
	articles_coll = db.articles
	articles=[]
	cursor = articles_coll.find()
	while (yield cursor.fetch_next):
		article = cursor.next_object()
		#print article
		art_obj = dict()
		art_obj['title']=article['name']
		art_obj['body']=tornado.escape.xhtml_escape(article['description'])
		art_obj['published']=article['time']
			# art_obj['publisheddate']=article['date']
		art_obj['author']=article['author']
		articles.append(art_obj)
		final_articles = {"articles":articles}
		yield final_articles
		#yield articles
		
		


#Handles /


class IndexHandler(BaseHandler):
	i=1
	@tornado.web.asynchronous
	@gen.coroutine
	

	def get(self):
		"""
		display list of articles
		"""
		final_articles=farticles(self)
		print"helooo"
		self.write(tornado.escape.json_encode(final_articles))
		
def farticles(self):
	key = 'blog_index'
	print "byee"
	final_articles= dict()
	
	articles = memcache.get(key)
	#if articles is None or IndexHandler.i==0:
		#articles_coll = self.application.db.articles
		#logging.error("hello")
		#articles=[]
		#cursor = articles_coll.find()
		#IndexHandler.i=1
		#while (yield cursor.fetch_next):
		#	article = cursor.next_object()
	#			#print article
	#		art_obj = dict()
	#		art_obj['title']=article['name']
	#		art_obj['body']=tornado.escape.xhtml_escape(article['description'])
	#		art_obj['published']=article['time']
	#		art_obj['author']=article['author']
	#		articles.append(art_obj)
	#		final_articles = {"articles":articles}
	#		print final_articles
	#		
	#	print "accessed db"
	#	mc.set(key,final_articles)

	#yield final_articles	




