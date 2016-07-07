from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.

class VisitorProfile(models.Model):
    user = models.OneToOneField(User, related_name='visitor')
    password = models.CharField(max_length = 50, blank = False)
    register = models.IntegerField(default='0')

    def __unicode__ (self):
    	return self.user.username


class Appointment(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, related_name = 'by')
	appointmentwith = models.ForeignKey(User, related_name = 'appointmentwith')
	on = models.DateField()	
	specialization = models.CharField(max_length = 100)
	service = models.CharField(max_length = 100,blank = True, null= True)
	comment = models.TextField(blank=True)
	time = models.TimeField()
	timestamp = models.DateTimeField(auto_now_add = True)

	def __unicode__ (self):
		return self.user.username + ' has appointment with ' + self.appointmentwith.username 

class Rating(models.Model):
	id = models.AutoField(primary_key=True)
	amount = models.IntegerField()
	of = models.ForeignKey(User, related_name = 'ofuser')
	by = models.ForeignKey(User, related_name = 'byuser')
	timestamp = models.DateTimeField(auto_now_add = True)

	def __unicode__ (self):
		return self.by.username + ' rated ' + self.of.username 
	
class Review(models.Model):
	id = models.AutoField(primary_key=True)
	text = models.TextField()
	of = models.ForeignKey(User, related_name = 'reviewofuser')
	by = models.ForeignKey(User, related_name = 'reviewbyuser')
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add = True)

	def __unicode__ (self):
		return self.by.username + ' rated ' + self.of.username 