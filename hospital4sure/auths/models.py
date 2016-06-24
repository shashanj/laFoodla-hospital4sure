from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import os

# Create your models here.

def getfolder(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=250,default=' ')
	membershhip_fees = models.IntegerField()

	def __unicode__ (self):
		return self.name

class SubCategory(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=250,default=' ')
	category = models.ForeignKey(Category)

	def __unicode__ (self):
		return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    password = models.CharField(max_length = 50, blank = False)
    category = models.ForeignKey(Category, related_name= 'category')
    subcategory = models.ForeignKey(SubCategory,blank=True,null=True,related_name='sub_Category')
    register = models.IntegerField(default='0')
    verfied = models.IntegerField(default='0')

    ######### contact details ############
    telephone = models.CharField(max_length = 20)
    username = models.CharField(max_length = 40,null=True,blank = True,unique=True)
    website = models.URLField(null=True,blank = True)

    def __unicode__ (self):
    	return self.user.username

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='address')
    type = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50,default='')
    district = models.CharField(max_length = 50)
    landmark = models.CharField(max_length = 50)
    street = models.CharField(max_length = 50)
    pincode = models.CharField(max_length=6)
    
    def __unicode__ (self):
        return self.user.username

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length = 100)
    Format = models.CharField(max_length = 100)
    MaxSize = models.IntegerField()
    amount = models.IntegerField(default=1)
    list_view = models.IntegerField(default=0)
    
    def __unicode__ (self):
        return self.name

class UserDocument(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,related_name = 'docsof')
    documnet = models.ForeignKey(Document)
    file = models.FileField(upload_to = getfolder)

    def __unicode__(self):
        return self.user.username + ' uploaded ' + self.documnet.name
class DisplayCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250,default='')

    def __unicode__ (self):
        return self.name
        
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ManyToManyField(Category)
    subcategory = models.ManyToManyField(SubCategory)
    title = models.CharField(max_length=100)
    options = models.TextField(blank = True)
    type = models.IntegerField()
    require = models.CharField(max_length = 10,blank = True)
    placeholder = models.CharField(max_length = 40, blank = True)
    order = models.IntegerField(default=0)
    formatType = models.CharField(max_length = 40, default='text',blank=True)
    disp = models.ManyToManyField(DisplayCategory)

    def __unicode__ (self):
        return self.title

class UserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.TextField(default='')
    question = models.ForeignKey(Question,related_name='questionof')
    user =  models.ForeignKey(User,related_name='answerby')

    def __unicode__(self):
        return self.user.username + ' answered ' + self.question.title



