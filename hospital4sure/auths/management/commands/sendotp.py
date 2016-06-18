from django.core.management.base import BaseCommand, CommandError
import urllib2 , urllib


class Command(BaseCommand):
	"""docstring for Command"""
	help = 'sendind otp to user'

	def add_arguments(self, parser):
		parser.add_argument('otp',type=str)


	def handle(self, *args, **options):
		otp,mobiles = options['otp'].split('.')
		authkey = "116152AVn4migBYw575f1ec6"
		message =  "Your verification code for Hospital4sure.com is: " + otp
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