from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def registration(self, form_data):
		firstname =[]
		lastname =[]
		email =[]
		password = []
		confirm =[]
		birth =[]
		boolerror = False
		if len(form_data['firstname'] ) < 4:
			firstname.append('*Name cannot be less than 4 characters')
			boolerror = True
		if len(form_data['lastname'] )< 4:
			lastname.append('*Alias cannot be less than 4 characters')
			boolerror = True
		if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)' , form_data['email']):
			email.append('*That is not a valid email format')
			boolerror = True
		duplicate = User.objects.filter(email = form_data['email']).first()
		if duplicate:
			email.append("That email has already been registered")
			boolerror = True
		if len(form_data['password'] ) == 0:
			password.append('*Password is required')
			boolerror = True
		if len(form_data['password'] ) < 8:
			password.append('*Password must be at least 8 characters')
			boolerror = True
		if form_data['password'] != form_data['confirm']:
			confirm.append('*Password doesn\'t match')
			boolerror = True
		if len(form_data['birth'] ) == 0:
			birth.append('*Birthdate is required')
			boolerror = True	
		errors = {
		'firstname':firstname,
		'lastname':lastname,
		'email':email,
		'password':password,
		'confirm':confirm,
		'boolerror':boolerror,
		'birth':birth,
		}
		return errors

	def validate(self,form_data):
		email =[]
		password = []
		boolerror = False
		if len(form_data['email']) == 0:
			email.append('*Email cannot be blank')
			boolerror = True
		if len(form_data['password']) == 0:
			password.append('*Password cannot be blank')
			boolerror = True
		varlogin = User.objects.filter(email=form_data['email']).first()
		if varlogin:
			userpassword = str(form_data['password'])
			db_password = str(varlogin.password)
			hashed_pw = bcrypt.hashpw(userpassword, db_password)
			if hashed_pw == db_password:
				boolerror = False
			else:
				password.append("*Password doesn't match our records")
				boolerror = True
		else:
			email.append("*Email address does not match our records")
			boolerror = True	
		errors = {
		'loginemail':email,
		'loginpassword':password,
		'boolerror':boolerror,
		'user': varlogin
		}
		return errors

	def create_user(self,form_data):
		password = str(form_data['password'])
		hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
		varuser = User.objects.create(firstname = form_data['firstname'],
						 alias = form_data['lastname'], 
						 email = form_data['email'], 
						 birthdate = form_data['birth'], 
						 password = hashed_pw)
		return varuser

class  User(models.Model):
	firstname = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	password = models.CharField(max_length=255)
	birthdate = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Poke(models.Model):
	poked_user = models.ForeignKey(User,related_name ="pokeduser", on_delete=models.CASCADE)
	poked_by = models.ForeignKey(User,related_name ="pokedby", on_delete=models.CASCADE)





