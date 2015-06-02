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



# handles registration of users
class RegisterHandler(BaseHandler):
	"""
		for registration of admins
	"""
	#@tornado.web.authenticated
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
		user = dict()
		user['name']=registername
		user['email']=registeremail
		user['password']=registerpassword

		yield users_coll.insert(user)
		self.render('register.html',name=registername,email=registeremail,password=registerpassword)




#handles for admin login
class LoginHandler(BaseHandler):
	"""
		handles logginf for admins
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



# handles admin logging out
class LogoutHandler(BaseHandler):
	"""
		handles logout for admins
	"""
	@tornado.web.authenticated
	def get(self):
		self.clear_cookie("email")
		self.redirect("/")