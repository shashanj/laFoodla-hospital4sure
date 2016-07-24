from django.shortcuts import render
from Internal.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def joinsms(name,position):

	message = name + ' wants to join for\n'
	for pos in position:
		message += Position.objects.get(id = pos).name + '\n'
	authkey = "116152AVn4migBYw575f1ec6"
	sender = "HOSPTL" # Sender I
	route = "4" # Define route
	values = {
				'authkey' : authkey,
				'mobiles' : '9425007971',
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


def join(request):
	if request.POST:
		name = request.POST.get('name')
		number = request.POST.get('number')
		collegename = request.POST.get('collegename')
		position = request.POST.getlist('option')

		emplyee = Employee()
		emplyee.name = name
		emplyee.number = number
		emplyee.collegename = collegename
		emplyee.save()
		for pos in position :
			if pos == 'other' :
				emplyee.additonal_position = request.POST.get('other')
			else:
				emplyee.position.add(pos)
		emplyee.save()
		import thread
		thread.start_new_thread(joinsms,(name,position))
		return HttpResponse('Received Your Request')

	options = Position.objects.all()
	return render_to_response('auth/join.html',{'options' : options},RequestContext(request))


def index(request):
	event = Event.objects.all()
	return render_to_response('visitor/event.html',{'events' : event},RequestContext(request))

def logineventuser(request):
	if 'eventuserid' in request.session :
			return HttpResponseRedirect('/event/dashboard/')

	if request.POST:
		num = request.POST.get('phone')
		try : 
			number = int(num)
		except:
			error = 'Enter a valid phone number'
			return render_to_response('visitor/eventlogin.html',{'error' : error},RequestContext(request))
		if len(num) != 10:
			error = 'Enter a valid phone number'
			return render_to_response('visitor/eventlogin.html',{'error' : error},RequestContext(request))

		pss = request.POST.get('password')

		try:
			user = LiveEventUser.objects.get(phone = num, password = pss)
			request.session['eventuserid'] = user.id
			return HttpResponseRedirect('/event/dashboard/')
		except Exception, e:
			print e
			error = 'Phone Number and/or Password Incorrect'
			return render_to_response('visitor/eventlogin.html',{'error' : error},RequestContext(request))			

	return render_to_response('visitor/eventlogin.html',RequestContext(request))


def dashboard(request):
	user = LiveEventUser.objects.get(id = request.session['eventuserid'])
	events = user.eventuser.all()
	for event in events :
		latest = event.details.split('\r\n')
		event.latest = latest[0]
	context = {
		'events' : events,
		'user' : user,
	}
	return render_to_response('visitor/dash.html',context,RequestContext(request))

def add(request):
	if request.POST:
		try : 
			event = Event()
			event.user = LiveEventUser.objects.get(id = request.session['eventuserid'])
			event.name = request.POST.get('name')
			event.video_link = request.POST.get('video')
			event.details = request.POST.get('details')
			event.photo = ''
			for url in request.POST.getlist('photo'):
				event.photo += url + '\r\n'
			event.save()
			return HttpResponseRedirect('/event/dashboard/')
		except:
			return render_to_response('visitor/addevent.html',{'error' : 'Something Went Wrong'}, RequestContext(request))

	return render_to_response('visitor/addevent.html', RequestContext(request))


def edit(request,id):
	event = Event.objects.get(id =id)

	if request.POST :
		event.name = request.POST.get('name')
		event.video_link = request.POST.get('video')
		event.details = request.POST.get('latest') + '\r\n'+ request.POST.get('details')
		event.photo = ''
		for url in request.POST.getlist('photo'):
			event.photo += url + '\r\n'
		try :
			event.save()
			return HttpResponseRedirect('/event/dashboard/')
		except : 
			return render_to_response('visitor/editevent.html',{'error' : 'Something Went Wrong'}, RequestContext(request))

	event.ph = event.photo.split('\r\n')
	return render_to_response('visitor/editevent.html',{'event' : event}, RequestContext(request))

def view(request,id):
	event = Event.objects.get(id =id)
	event.ph = event.photo.split('\r\n')
	return render_to_response('visitor/viewevent.html',{'event' : event}, RequestContext(request))

def logouteventuser(request):
	try :
		del request.session['eventuserid']
	except :
		pass
	return HttpResponseRedirect('/')