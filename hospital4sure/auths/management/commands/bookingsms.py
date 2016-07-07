from django.core.management.base import BaseCommand, CommandError
import urllib2 , urllib
from visitor.models import *
from django.contrib.auth.models import User
from datetime import datetime
class Command(BaseCommand):
	"""docstring for Command"""
	help = 'send booking sms to user'

	def add_arguments(self, parser):
		parser.add_argument('id',type=str)


	def handle(self, *args, **options):
		
		appointment_id = options['id']
		appointment = Appointment.objects.get(id = appointment_id)
		print options['id'],str(appointment.time)
		mobiles = appointment.appointmentwith.username
		authkey = "116152AVn4migBYw575f1ec6"
		message =  "New Appointment Booked By " + appointment.user.first_name + appointment.user.last_name  + ' on ' + datetime.strftime(appointment.on,'%d/%m/%Y') + ' at ' + str(appointment.time) + ' for ' + appointment.specialization + '. Kindly Contact them at '+ appointment.user.username
		sender = "HOSPTL" # Sender I
		route = "4" # Define route

		values = {
	              'authkey' : authkey,
	              'mobiles' : mobiles,
	              'message' : message,
	              'sender' : sender,
	              'route' : route,
		}
		url = "https://control.msg91.com/api/sendhttp.php"
		postdata = urllib.urlencode(values)
		try :
			req = urllib2.Request(url, postdata)
			response = urllib2.urlopen(req)
			output = response.read() # Get Response
			print output
		except Exception, e:
			print e

		print 'message to corporate profile send'



		############# normal user #############################
		mobiles = appointment.user.username
		name = appointment.appointmentwith.answerby.filter(question__order = 1)[0].answer
		message =  "Your Appointment with " + name + ' on ' + datetime.strftime(appointment.on,'%d/%m/%Y') + ' at ' + str(appointment.time) + ' for ' + appointment.specialization + ' is booked.'
		values = {
	              'authkey' : authkey,
	              'mobiles' : mobiles,
	              'message' : message,
	              'sender' : sender,
	              'route' : route,
		}
		url = "https://control.msg91.com/api/sendhttp.php"
		postdata = urllib.urlencode(values)
		try :
			req = urllib2.Request(url, postdata)
			response = urllib2.urlopen(req)
			output = response.read() # Get Response
			print output
		except Exception, e:
			print e

		print 'message to normal user send'
