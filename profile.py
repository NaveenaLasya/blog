import tornado.web

import pymongo
import motor
import json
import jwt

import hashlib
from Crypto.Hash import SHA256

from tornado import gen
from bson import json_util
from bson.json_util import dumps

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



# handles registration of users
class RegisterHandler(BaseHandler):
	"""
		Handles registration of admins
	"""

	def get(self):
		self.render('register.html')


	@tornado.web.asynchronous
	@gen.coroutine
	def post(self):
		users_coll = self.application.db.users 
		registername=self.get_argument("registername")
		registeremail=self.get_argument("registeremail")
		registerpassword=self.get_argument("registerpassword")
		registerpassword=SHA256.new(registerpassword).hexdigest()
		registertoken=jwt.encode({'registerpassword':registerpassword},'cookie_secret',algorithm='HS256',headers={'registeremail':registeremail})
		user = dict()
		user['name']=registername
		user['email']=registeremail
		user['password']=registerpassword
		user['token']=registertoken

		yield users_coll.insert(user)
		self.render('register.html',name=registername,email=registeremail,password=registerpassword)

class AndroidLoginHandler(BaseHandler):
	@tornado.web.asynchronous
	@gen.coroutine	
	def get(self):
		#self.render('login.html')
		user_details=dict()
		users_coll = self.application.db.users 
		loginemail=self.get_argument("loginemail")
		loginpassword=self.get_argument("loginpassword")
		currentuser=yield users_coll.find_one({'email':loginemail,})
		if currentuser: 
			loginpassword=SHA256.new(loginpassword).hexdigest()
			if loginpassword==currentuser['password']:
				currentusername=currentuser['name']
				self.set_secure_cookie("email",loginemail)
				user_details=dict()
				user_details['token'] = currentuser['token']
				user_details['email'] = currentuser['email']
				user_details['Success'] = "1"
			else:
				user_details['message'] = "username"
				user_details['Success'] = "False"
			self.write(json.loads(json_util.dumps(user_details)))	
		else:
			self.write("please register")




#handles for admin login
class LoginHandler(BaseHandler):
	"""
		handles login for admins
	"""
	def get(self):
		self.render('login.html')
		

	@tornado.web.asynchronous
	@gen.coroutine	
	def post(self):

		users_coll = self.application.db.users 
		loginemail=self.get_argument("loginemail")
		loginpassword=self.get_argument("loginpassword")
		currentuser=yield users_coll.find_one({'email':loginemail,})
		if currentuser: 
			loginpassword=SHA256.new(loginpassword).hexdigest()
			if loginpassword==currentuser['password']:
				currentusername=currentuser['name']
				self.set_secure_cookie("email",loginemail)
				self.redirect('/')
			else:
				self.write("hey please enter the pass word correctly")
		else:
			self.write("please register")


class ErrorHandler(BaseHandler):
	def get(self):
		self.write("404")



# handles admin logging out
class LogoutHandler(BaseHandler):
	"""
		handles logout for admins
	"""
	@tornado.web.authenticated
	def get(self):
		self.clear_cookie("email")
		self.redirect("/")