from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from App.decorators import is_logged_In
from django.db.models import Count
from .models import *
from . import accountSettings
import uuid
import datetime
from django.contrib import messages


# Create your views here.

def index(request):
	recentQuestions = Questions.objects.all().order_by('-date')
	Ans = []
	for qid in recentQuestions:
		allAnswers = Answers.objects.filter(question=qid)
		Ans.append(allAnswers)
	if request.session.has_key('user'):
		user = request.session['user']
		params = {'userloggedIn':user,'AllQuestions':zip(recentQuestions,Ans),'class_':'recent',}
	else:
		params = {'AllQuestions':zip(recentQuestions,Ans),'class_':'recent'}
	return render(request, "index.html", params)

def about(request):
	if request.session.has_key('user'):
		user = request.session['user']
		params = {'userloggedIn':user}
	else:
		params = {}
	return render(request, "about.html", params)

def contactus(request):
	if request.session.has_key('user'):
		user = request.session['user']
		params = {'userloggedIn':user}
	else:
		params = {}
	return render(request, "contactus.html", params)

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

@is_logged_In
def answer(request,id):
	questionData = Questions.objects.get(questionId=id)
	AllAnswers = Answers.objects.filter(question_id=questionData)
	all_Users = []
	count=''
	for question in  Questions.objects.filter(questionId=id):
		count = str(question.Views)
	view_count = str(int(count)+1)
	print(view_count)
	datasave = Questions.objects.filter(questionId=id).update(Views=view_count)
	for userid in AllAnswers:
		fName = UserDetail.objects.get(UserId=userid.User).FirstName
		lName = UserDetail.objects.get(UserId=userid.User).LastName
		all_Users.append(fName+' '+lName)
	params = {'AllAnswers':zip(AllAnswers,all_Users),'questionData':questionData}
	return render(request,'answers.html', params)

@csrf_exempt
def postanswer(request):
	qid = request.POST.get('questionId')
	answer = request.POST.get('answer')
	answerId = uuid.uuid4()
	questionObj = Questions.objects.get(questionId=qid)
	answerObj = Answers(answerId=answerId,question=questionObj,answer=answer,totalVotes=0,User=request.session['user'])
	answerObj.save()
	
	return HttpResponseRedirect('/answer/'+qid+'/')

def recent(request):
	recentQuestions = Questions.objects.all().order_by('-date')
	Ans = []
	for qid in recentQuestions:
		allAnswers = Answers.objects.filter(question=qid)
		Ans.append(allAnswers)
	if request.session.has_key('user'):
		user = request.session['user']
		params = {'userloggedIn':user,'AllQuestions':zip(recentQuestions,Ans),'class_':'recent'}
	else:
		params = {'AllQuestions':zip(recentQuestions,Ans),'class_':'recent'}
	return render(request,'index.html',params)

def mostAnswered(request):
	mostAnswered = Questions.objects.annotate(count=Count('answers')).order_by('-count')
	Ans = []
	for qid in mostAnswered:
		allAnswers = Answers.objects.filter(question=qid)
		Ans.append(allAnswers)
	if request.session.has_key('user'):
		user = request.session['user']
		params = {'userloggedIn':user,'AllQuestions':zip(mostAnswered,Ans),'class_':'mostAnswered'}
	else:
		params = {'AllQuestions':zip(mostAnswered,Ans),'class_':'mostAnswered'}
	return render(request,'index.html',params)

def mostVisited(request):
	mostVisited = Questions.objects.annotate(count=Count('Views')).order_by('-count')
	Ans = []
	for qid in mostVisited:
		allAnswers = Answers.objects.filter(question=qid)
		Ans.append(allAnswers)
	if request.session.has_key('user'):
		user = request.session['user']
		params = {'userloggedIn':user,'AllQuestions':zip(mostVisited,Ans),'class_':'mostVisited'}
	else:
		params = {'AllQuestions':zip(mostVisited,Ans),'class_':'mostVisited'}
	return render(request,'index.html',params)

def mostPopular(request):
	mostPopular = Questions.objects.all().order_by('-totalVotes','-Views')
	Ans = []
	for qid in mostPopular:
		allAnswers = Answers.objects.filter(question=qid)
		Ans.append(allAnswers)
	if request.session.has_key('user'):
		user = request.session['user']
		params = {'userloggedIn':user,'AllQuestions':zip(mostPopular,Ans),'class_':'mostPopular'}
	else:
		params = {'AllQuestions':zip(mostPopular,Ans),'class_':'mostPopular'}
	return render(request,'index.html',params)

def profile(request, id):
	userInfo = UserDetail.objects.get(UserId=id)
	params = {'user':userInfo}
	return render(request, 'Profile.html', params)

def search(request):
	flag = False
	
	query = request.GET['search']

	if query == '':
		allQuestions = Questions.objects.none()
	elif len(query)>20:
		allQuestions = Questions.objects.none()
	else:
		allQuestions = Questions.objects.filter(question__icontains=query)
		Ans = []
		for qid in allQuestions:
			allAnswers = Answers.objects.filter(question=qid)
			Ans.append(allAnswers)
		print(Ans)
		#allposts = allPostTitle.union(allPostCategory,allPostChannel_Name)
	if allQuestions.count() == 0:
		messages.warning(request,'No search results found. Please refine your query')
	if request.session.has_key('user'):
		flag = True
		user = request.session['user']
		userPic = UserDetail.objects.filter(UserId=request.session['user'])
		params = {'allQuestions':zip(allQuestions,Ans),'query':query,'flag':flag,'image':userPic,'Questions':allQuestions,'userloggedIn':user}
	else:
		params = {'allQuestions':zip(allQuestions,Ans),'query':query,'flag':flag,'Questions':allQuestions}
	return render(request,'search.html',params)