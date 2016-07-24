from django.db import models

# Create your models here.

class Position(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length = 100)

	def __unicode__ (self):
		return self.name
		

class Employee(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 40)
	mobile = models.CharField(max_length = 18)
	college = models.CharField(max_length = 150)
	position = models.ManyToManyField(Position)
	additional_position = models.CharField(max_length=100, blank= True, null = True)
	
	def __unicode__ (self):
		return self.name


class LiveEventUser(models.Model):
	id = models.AutoField(primary_key = True)
	phone = models.CharField(max_length = 10, unique = True)
	name = models.CharField(max_length = 40)
	password = models.CharField(max_length = 40)

	def __unicode__(self):
		return self.phone

class Event(models.Model):
	id = models.AutoField(primary_key = True)
	user = models.ForeignKey(LiveEventUser, related_name = 'eventuser')
	name = models.CharField(max_length = 40)
	details = models.TextField()
	video_link = models.URLField()
	photo = models.TextField()
	timestamp = models.DateTimeField(auto_now_add = True)
	
	def __unicode__ (self):
		return self.name
		