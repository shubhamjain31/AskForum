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
from django.db.models import Case, Value, When


# Create your views here.

def error_404_view(request):
	return render(request, "404.html")

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

@csrf_exempt
def vote(request):	
	questionId = request.POST.get('questionId')
	action = request.POST.get('action')

	question_posted_by = Questions.objects.get(questionId=questionId).User.UserId
	score_of_person_voting = UserDetail.objects.get(UserId=request.session['user']).Score
	question_owner_score = Questions.objects.get(questionId=questionId).User.Score
	print(score_of_person_voting)

	if question_posted_by == request.session['user']:
		return JsonResponse({'Response':"You can't vote your own Question",'flag':False})
	elif score_of_person_voting < 10:
		return JsonResponse({'Response':"You don't have enough score!",'flag':False})
		
	if action == 'up':
		voteType = 1
		total_score_change = 10
	elif action == 'down':
		voteType = -1
		total_score_change = -10
	else:
		pass

	voteRecord = QuestionVotes.objects.filter(questionId=questionId,userId=request.session['user'])

	upVoteRecord = voteRecord.filter(voteType=1)

	downVoteRecord = voteRecord.filter(voteType=-1)

	voteCount = Questions.objects.get(questionId=questionId).totalVotes

	if upVoteRecord and action == 'up':
		print('1')
		msg = 'Already Upvoted'; count = 0
		pass
	elif upVoteRecord and action == 'down':
		print('2')
		msg = 'You downvoted this question'; count = -1
		Questions.objects.filter(questionId=questionId).update(totalVotes=voteCount - 1)
		UserDetail.objects.filter(UserId=question_posted_by).update(Score = question_owner_score + total_score_change)


	elif downVoteRecord and action == 'down':
		print('3')
		msg = 'Already Downvoted'; count = 0
		pass
	elif downVoteRecord and action == 'up':
		print('4')
		msg = 'You upvoted this question'; count = 1
		Questions.objects.filter(questionId=questionId).update(totalVotes=voteCount + 1)
		UserDetail.objects.filter(UserId=question_posted_by).update(Score = question_owner_score +total_score_change)

	if voteRecord and action == 'up':
		QuestionVotes.objects.filter(questionId=questionId,userId=request.session['user']
		).update(voteType=Case(
			When(voteType=1, then=Value(1)),
			When(voteType=-1,then=Value(1)),
		))
		
	elif voteRecord and action == 'down':
		QuestionVotes.objects.filter(questionId=questionId,userId=request.session['user']
		).update(voteType=Case(
			When(voteType=1, then=Value(-1)),
			When(voteType=-1,then=Value(-1)),
		))
		
	else:
		QuestionVotes(questionId=questionId,userId=request.session['user'],voteType=voteType).save()
		Questions.objects.filter(questionId=questionId).update(totalVotes = voteCount + voteType)
		msg = 'You ' + action + 'voted this question'; count = voteType
		UserDetail.objects.filter(UserId=question_posted_by).update(Score = question_owner_score +total_score_change)
	outcome = {'Response':msg,'count':count,'action':action}

	return JsonResponse(outcome)

@csrf_exempt
def answervote(request):
	questionid = request.POST.get('questionId')
	answerid = request.POST.get('answerId')
	action = request.POST.get('action')	
	
	score_of_person_voting = UserDetail.objects.get(UserId=request.session['user']).Score
	
	questionObj = Questions.objects.get(questionId=questionid)
	allAnswers = Answers.objects.filter(question=questionObj)
	for ans in allAnswers:
		if str(ans.answerId) == answerid:	
			voteCount =  ans.totalVotes
			answer_posted_by = ans.User
			answer_owner_score = UserDetail.objects.get(UserId=answer_posted_by).Score
			break
	if answer_posted_by == request.session['user']:
		return JsonResponse({'Response':"You can't vote your own Answer",'flag':False})
	elif score_of_person_voting < 0:
		return JsonResponse({'Response':"You don't have enough score!",'flag':False})

	if action == 'up':
		voteType = 1
		total_score_change = 10
	elif action == 'down':
		voteType = -1
		total_score_change = -10
	else:
		pass

	voteRecord = AnswerVotes.objects.filter(answerId=answerid,userId=request.session['user'])
	
	upVoteRecord = voteRecord.filter(voteType=1)
	
	downVoteRecord = voteRecord.filter(voteType=-1)
	
	
	if upVoteRecord and action == 'up':
		print('1')
		msg = 'Already Upvoted'; count = 0
		pass
	
	elif upVoteRecord and action == 'down':
		print('2')
		msg = 'You downvoted this answer'; count = -1
		ans.totalVotes -= 1				
		questionObj.save()
		UserDetail.objects.filter(UserId=answer_posted_by).update(Score = answer_owner_score + total_score_change)
	
	elif downVoteRecord and action == 'down':
		print('3')
		msg = 'Already Downvoted'; count = 0
		pass
	
	elif downVoteRecord and action == 'up':
		print('4')
		msg = 'You upvoted this answer'; count = 1
		ans.totalVotes += 1
		
		questionObj.save()
		UserDetail.objects.filter(UserId=answer_posted_by).update(Score = answer_owner_score + total_score_change)

	if voteRecord and action == 'up':
		AnswerVotes.objects.filter(answerId=answerid,userId=request.session['user']
		).update(voteType=Case(
			When(voteType=1, then=Value(1)),
			When(voteType=-1,then=Value(1)),
		))
		
	elif voteRecord and action == 'down':
		AnswerVotes.objects.filter(answerId=answerid,userId=request.session['user']
		).update(voteType=Case(
			When(voteType=1, then=Value(-1)),
			When(voteType=-1,then=Value(-1)),
		))
		
	else:
		AnswerVotes(answerId=answerid,userId=request.session['user'],voteType=voteType).save()
		
		ans.totalVotes += voteType
		
		questionObj.save()
		msg = 'You ' + action + 'voted this question'; count = voteType
		UserDetail.objects.filter(UserId=answer_posted_by).update(Score = answer_owner_score +total_score_change)
	return JsonResponse({'Response':msg,'count':count,'action':action})