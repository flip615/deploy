from django.shortcuts import render, redirect
from .models import *
import bcrypt

def main(request):
	if 'user' in request.session:
		return redirect('/pokes')
	if 'errors' not in request.session:
		request.session['errors'] = {}
	context = request.session['errors']
	request.session.pop('errors')
	return render(request,'new_app/main.html',context)

def registration(request):
	if request.method =="POST":
		form_data = request.POST
		varerror = User.objects.registration(form_data)
		request.session['errors'] = varerror
		if not varerror['boolerror']:
			varuser = User.objects.create_user(form_data)
			request.session['user'] = varuser.id
			return redirect('/pokes')
		else:
			return redirect('/')
	return redirect('/')		

def login(request):
	if request.method == "POST":
		form_data = request.POST
		validate = User.objects.validate(form_data)
		if not validate['boolerror']:
			request.session['user'] = validate['user'].id
			return redirect('/pokes')
		else:	
			errors = {
				'loginemail':validate['loginemail'],
				'loginpassword':validate['loginpassword'],
				}
			request.session['errors'] = errors
			pass
	return redirect('/')	

def pokes(request):
	if 'user'	 in request.session:
		user = User.objects.filter(id = request.session['user']).first()
		otherusers = User.objects.exclude(id = user.id)
		countpokes = Poke.objects.raw("""SELECT id, count(Distinct poked_by_id) as total
							FROM new_app_poke p 
							where poked_user_id = %s""", [user.id])
	
		allpokes = Poke.objects.raw("""SELECT user.id, user.firstname, user.alias, user.email, count(p.poked_by_id) as total
							FROM new_app_user as user
							left join new_app_poke as p 
							on user.id = p.poked_user_id
							group by user.id, user.firstname, user.alias, user.email """)

		listpokes = Poke.objects.raw("""SELECT  p. id, p.poked_by_id,  user.firstname, count(p.poked_by_id) as total
							FROM new_app_poke p
							join new_app_user as user
							on p.poked_by_id = user.id
							where p.poked_user_id = %s
							group by p.poked_by_id,  user.firstname
							order by total desc""", [user.id])
		
		context = {
		'user': user,
		'otherusers':otherusers,
		'pokes': pokes,
		'userpokes': countpokes,
		'allpokes':allpokes,
		'listpokes': listpokes
		}
	return render(request, 'new_app/pokes.html', context)

def logout(request):
	request.session.flush()
	return redirect('/')

def addpoke(request,id):
	if str(request.session['user']) != str(id):
		varuser = Poke.objects.create(poked_user_id = id, poked_by_id = request.session['user'])
		return redirect('/pokes')
	return redirect('/pokes')






