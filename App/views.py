from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from .models import *
from . import accountSettings
import uuid
import datetime
from django.contrib import messages


# Create your views here.

def index(request):
	recentQuestions = Questions.objects.all().order_by('-date')
	if request.session.has_key('user'):
		user = request.session['user']
		params = {'userloggedIn':user,'AllQuestions':recentQuestions,'class_':'recent'}
	else:
		params = {'AllQuestions':recentQuestions,'class_':'recent'}
	return render(request, "index.html", params)

@csrf_exempt
def sessionval(request):
	if request.session.has_key('user'):
		return JsonResponse({'Result':True})
	else:
		return JsonResponse({'Result':False})

def register(request):
	if request.session.has_key('user'):
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			fName = request.POST.get('fName')
			lName = request.POST.get('lName')
			
			email = request.POST.get('email')
			mobile = request.POST.get('mobile')
			password = request.POST.get('password')
			confirmPassword = request.POST.get('confirmPassword')
			gender = request.POST.get('gender')[0]
			securityQuestion = request.POST.get('securityQuestion')
			securityAnswer = request.POST.get('securityAnswer')

			account_register_report = accountSettings.registerNewAccount(
				fName=fName,lName=lName,email=email,mobile=mobile,password=password,confirmPassword=confirmPassword,
				gender=gender,securityQuestion=securityQuestion,securityAnswer=securityAnswer
			)
			messages.success(request,account_register_report)
			return render(request,'registerAccount.html')
		else:
			return render(request,'registerAccount.html')

def login(request):
	if request.method == 'POST':
		email = request.POST.get("email")
		password = request.POST.get("password")
		login_status = accountSettings.loginToAccount(
			email=email,password=password
		)
		if not login_status:
			return render(request,'signin.html',{'message':'Please Check Your Email and Password'})
		else:
			request.session['user'] = login_status
			return HttpResponseRedirect('/')
		
	else:
		if request.session.has_key('user'):
			return HttpResponseRedirect('/')
		else:
			return render(request,'signin.html')

def logout(request):
	if request.session.has_key('user'):
		del request.session['user']
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

@csrf_exempt
def askaquestion(request):
	questionVal = request.POST.get('questionValue')
	user = UserDetail.objects.get(UserId=request.session['user'])
	Questions(question=questionVal,User=user).save()
	return JsonResponse({'Result':'Success'})