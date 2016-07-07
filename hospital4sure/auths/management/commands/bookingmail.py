from django.core.management.base import BaseCommand, CommandError
import urllib2 , urllib
from visitor.models import *
from django.contrib.auth.models import User
from datetime import datetime
import sendgrid
from hospital4sure.settings import EMAIL_HOST_USER as sg_username, EMAIL_HOST_PASSWORD as sg_password

class Command(BaseCommand):
	"""docstring for Command"""
	help = 'send booking email to users'

	def add_arguments(self, parser):
		parser.add_argument('id',type=str)


	def handle(self, *args, **options):
		
		appointment_id = options['id']
		appointment = Appointment.objects.get(id = appointment_id)
		body = 'Hello '+ appointment.user.first_name + ' ' + appointment.user.last_name  +',<br>'
		body += '<h3>Booking Details</h3> <br>'
		body += '<table style="width:100%"><tr><td style="text-align:middle">Name</td> <td style="text-align:middle">' + appointment.appointmentwith.answerby.filter(question__order = 1)[0].answer + '</td></tr>'
		body += '<tr><td style="text-align:middle">Date</td><td style="text-align:middle">' + datetime.strftime(appointment.on,'%d/%m/%Y') + '</td></tr>'
		body += '<tr><td style="text-align:middle">Time</td><td style="text-align:middle">' + str(appointment.time) + '</td><tr>'
		body += '<tr><td style="text-align:middle">Specialzation</td><td style="text-align:middle">' + appointment.specialization + '</td><tr>'
		
		sg = sendgrid.SendGridClient(sg_username, sg_password)
		message = sendgrid.Mail()
		message.set_from("shashanks.1903@gmail.com")
		message.set_subject("New Appointment")
		message.set_text("This is text body")
		message.set_html(body)
		message.add_to(appointment.user.email)
		status, msg = sg.send(message)
		print status,msg


		########## send mail to corporate ###############
		sg = sendgrid.SendGridClient(sg_username, sg_password)

		messag = 'Hello '+ appointment.appointmentwith.answerby.filter(question__order = 1)[0].answer  +',<br>'
		messag += '<h3>Booking Details</h3> <br>'
		messag += '<table style="width:100%"><tr><td style="text-align:middle">Name</td> <td style="text-align:middle">' + appointment.appointmentwith.answerby.filter(question__order = 1)[0].answer + '</td></tr>'
		messag += '<tr><td style="text-align:middle">Date</td><td style="text-align:middle">' + datetime.strftime(appointment.on,'%d/%m/%Y') + '</td></tr>'
		messag += '<tr><td style="text-align:middle">Time</td><td style="text-align:middle">' + str(appointment.time) + '</td><tr>'
		messag += '<tr><td style="text-align:middle">Specialzation</td><td style="text-align:middle">' + appointment.specialization + '</td><tr>'
		messag += '<tr><td style="text-align:middle">Contact Detail</td><td style="text-align:middle">' + appointment.user.username + '</td><tr></table>'
		

		message = sendgrid.Mail()
		message.set_from("shashanks.1903@gmail.com")
		message.set_subject("New Appointment")
		message.set_text("This is text body")
		message.set_html(messag)
		message.add_to(appointment.appointmentwith.email)
		status, msg = sg.send(message)
		print status,msg
