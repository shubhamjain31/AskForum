from django.db import models
from datetime import datetime
from django_mysql.models import ListCharField
import uuid

class UserDetail(models.Model):
	UserId = models.CharField(max_length=50,default='',blank=True)
	FirstName = models.CharField(max_length=50,default='',blank=True)
	LastName = models.CharField(max_length=50,default='',blank=True)
	Phone = models.CharField(max_length=10,default='',blank=True)
	Password = models.CharField(max_length=100,default='',blank=True)
	Email = models.EmailField(blank=True)
	SecurityQuestion = models.CharField(max_length=150,default='',blank=True)
	SecurityAnswer = models.CharField(max_length=500,default='',blank=True)
	profilePic = models.ImageField(upload_to='media', default='media/user.png')
	Score = models.IntegerField(default=0)
	MALE = 'M'
	FEMALE = 'F'
	OTHER = 'O'
	GENDER_CHOICES = [
	    (MALE, 'Male'),
	    (FEMALE, 'Female'),
	    (OTHER, 'Other')
	    ]
	Gender = models.CharField(max_length=1,default='',choices=GENDER_CHOICES)
	date = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.FirstName+' '+self.LastName

class Questions(models.Model):
	questionId = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
	question = models.TextField()
	totalVotes = models.IntegerField(default=0,blank=True)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	Views = models.IntegerField(default=0)
	User = models.ForeignKey(UserDetail,on_delete=models.CASCADE,related_name='userinfo')
	
	def __str__(self):
		return str(self.questionId)

class Answers(models.Model):
	answerId = models.CharField(max_length=100,default='', unique=True)
	question = models.ForeignKey(Questions,on_delete=models.CASCADE)
	answer = models.TextField(blank=True)
	totalVotes = models.IntegerField(blank=True)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	User = models.CharField(max_length=50,blank=True,default='')

	def __str__(self):
		return str(self.answerId)

class QuestionVotes(models.Model):
	questionId = models.CharField(max_length=100,blank=True)
	userId = models.CharField(max_length=50)
	voteType = models.IntegerField(blank=True)		# -1 for down 1 for up

	def __str__(self):
		return str(self.questionId)

class AnswerVotes(models.Model):
	answerId = models.CharField(max_length=100,blank=True)
	userId = models.CharField(max_length=50)
	voteType = models.IntegerField(blank=True)		# -1 for down 1 for up

	def __str__(self):
		return str(self.answerId)