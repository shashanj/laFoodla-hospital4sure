from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core import management
from auths.management.commands import sendotp
from visitor.models import *
from auths.models import *
import random, string, json, re, urllib2 , urllib, ast
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def comcall(message):
    management.call_command('sendotp',message, verbosity=0)
    print 'message sent'

def bookingsms(id):
    management.call_command('bookingsms',str(id), verbosity=0)

def bookingmail(id):
    management.call_command('bookingmail',str(id), verbosity=0)

def getweeklist(weeks):
    add = []
    for week in weeks : 
        if 'mo' in week :
            add.append(0)
        elif 'tu' in week :
            add.append(1)
        elif 'we' in week : 
            add.append(2)
        elif 'th' in week :
            add.append(3)
        elif 'fr' in week :
            add.append(4)
        elif 'sa' in week :
            add.append(5)
        elif 'su' in week :
            add.append(6)
    return add


def index(request):
    try:
        del request.session['count']
        del request.session['otp']
        del request.session['change']
    except:
        pass

    if 'userid' not in request.session:
        id = [1,2,4,3,5]
        cat_id = Category.objects.filter(id__in = id)
        for cat in cat_id:
            cat.spec = Question.objects.filter(category = cat).filter(title = 'Specialization')[0].options.split('\r\n')
        context = {
            'cat' : cat_id,
            'userid' : -1,
        }
        return render_to_response('visitor/index.html',context,RequestContext(request))

    user = User.objects.get(id = request.session['userid'])
    profile =  user.visitor
    
    if profile.register == 0 :
        return HttpResponse('Your Mobile Number Is not Yet Verified. <a href="/user/sendotp/">Click Here</a> To verify.')

    id = [1,2,4,3,5]
    cat_id = Category.objects.filter(id__in = id)
    for cat in cat_id:
        cat.spec = Question.objects.filter(category = cat).filter(title = 'Specialization')[0].options.split('\r\n')
    context = {
        'cat' : cat_id,
        'userid' : 1,
        'user' : user,
    }
    return render_to_response('visitor/index.html',context,RequestContext(request))


def signup(request):
    try:
        del request.session['count']
        del request.session['otp']
        del request.session['change']
    except:
        pass
    return render_to_response('visitor/signup.html',RequestContext(request))

def signupprocess(request):
    if request.POST:
        try:
            username = request.POST.get('username')
            isd = request.POST.get('isd')

            if len(username) != 10 :
                error = 'Phone Number should be of 10 Digits'
                return render_to_response('visitor/signup.html',{'error' : error},RequestContext(request))

            try :
                print int(username)
            except :
                error = 'Phone Number Only has Digits'
                return render_to_response('visitor/signup.html',{'error' : error},RequestContext(request))
            
            if (User.objects.filter(username = isd + username).exists()):
                error = 'Phone Number already Registered Try Login'
                return render_to_response('visitor/signup.html',{'error' : error},RequestContext(request))
        except Exception, e:
            print e
            error = 'Phone Number Not Entered'
            return render_to_response('visitor/signup.html',{'error' : error},RequestContext(request))

        try :
            print request.POST.get('email')
            email = request.POST.get('email')
        except Exception,e :
            error = 'Please Enter A valid Email id'
            return render_to_response('visitor/signup.html',{'error' : error},RequestContext(request))

        password = request.POST.get('password')
        cp = request.POST.get('cp')
        
        if cp != password :
            error = 'Password Didnt Match '
            context = {
                'error': error,
            }
            return render_to_response('visitor/signup.html',context,RequestContext(request))

        fn = request.POST.get('fn')
        ln = request.POST.get('ln')

        new = User()
        new.username = isd + username
        new.first_name = fn
        new.last_name = ln
        new.save()
        new.set_password(password)
        new.email = email
        new.save()
        profile = VisitorProfile()
        profile.user = new
        profile.password = password
        profile.save()

        user = authenticate(username=isd + username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['userid'] = user.id
                print 'logged in'

        return HttpResponseRedirect('/user/sendotp/')

@login_required(login_url='/user/login/')
def sendotp(request):
    user = User.objects.get(id = request.session['userid'])
    if 'count' in request.session :
        if request.session['count'] > 3:
            error = 'Please Try Later Your Account is Temporarly Deactivated'
            user.is_active = False
            user.save()
            return render_to_response('visitor/verification.html',{'error': error}, RequestContext(request))

    if request.POST:
        if request.POST.get('otp') == request.session['otp'] : 
            user.visitor.register = 1 
            user.visitor.save()
            try:
                del request.session['count']
                del request.session['otp']
                del request.session['change']
            except:
                pass
            return HttpResponseRedirect('/user/')
        else :
            request.session['count'] += 1
        return render_to_response('visitor/verification.html', RequestContext(request))

    if 'otp' in request.session:
        return render_to_response('visitor/verification.html', RequestContext(request))

    otp = ''.join(random.choice(string.digits) for i in range(6))
    request.session['otp'] = otp
    request.session['count'] = 1
    request.session['change'] = 1
    print request.session['otp']

    username = user.username
    data = otp + '.' + username

    import thread
    thread.start_new_thread(comcall,(data,))

    return render_to_response('visitor/verification.html', RequestContext(request))

def logoutuser(request):
    try:
        del request.session['count']
        del request.session['otp']
        del request.session['change']
    except:
        pass
    del request.session['userid']
    logout(request)
    return HttpResponseRedirect('/')

def loginuser(request):
    try:
        del request.session['count']
        del request.session['otp']
        del request.session['change']
    except:
        pass

    if request.POST:
        phone = request.POST.get('phone')
        isd = request.POST.get('isd')
        username = isd+phone
        password = request.POST.get('password')
                
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['userid']=user.id
                    state = "login successfull"

                    if user.visitor.register == 0 :
                        return HttpResponse('Your Mobile Number Is not Yet Verified. <a href="/user/sendotp/">Click Here</a> To verify.')
                    return HttpResponseRedirect('/user/')
                else:
                    state = "your account is not active"
            else:
                state = 'your username and/or password was wrong'
        else:
            state = 'No such user exists'

        return render_to_response('visitor/login.html', {'error': state}, RequestContext(request))
    return render_to_response('visitor/login.html', RequestContext(request))

def changeotp(request):
    if request.is_ajax():
        if request.session['change'] < 4:
            request.session['change'] = request.session['change'] + 1
            user = User.objects.get(id = request.session['userid'])
            username = user.username
            otp = request.session['otp']
            data = otp + '.' + username
            import thread
            thread.start_new_thread(comcall,(data,))
            return HttpResponse('sent otp again')

        else :
            return HttpResponse('already sent 3 times Max limit reached')
    else :
        pass


def checkph(request):
    if request.POST:
        if request.POST.get('type') == 'phone':            
            try:
                username = request.POST.get('isd') + request.POST.get('phone')
                user = User.objects.get(username = username)
                otp = ''.join(random.choice(string.digits) for i in range(6))
                request.session['otp'] = otp
                request.session['count'] = 1
                request.session['change'] = 1
                print request.session['otp']

                username = user.username
                data = otp + '.' + username

                import thread
                thread.start_new_thread(comcall,(data,))
                
                return render_to_response('visitor/changecp.html',{'otp':'otp', 'user': user.id},RequestContext(request))
                

            except Exception, e:
                print e
                return render_to_response('visitor/changecp.html',{'phone':'phone', 'error' : 'Phone Nunmber Does Not Exist'},RequestContext(request))
        
        if request.POST.get('type') == 'otp':
            user = request.POST.get('user')    
            if 'count' in request.session :
                if request.session['count'] > 3:
                    return render_to_response('visitor/changecp.html',{'user':user,'error' : 'Failed to verify 3 times Contact Site Admin','otp':'otp'}, RequestContext(request))

            if request.POST:
                try : 
                    if request.POST.get('otp') == request.session['otp']: 
                        try:
                            del request.session['count']
                            del request.session['otp']
                            del request.session['change']
                        except:
                            pass
                        return render_to_response('visitor/changecp.html ',{'user':user,'pass': 'pass'},RequestContext(request))
                    else :
                        request.session['count'] += 1
                        return render_to_response('visitor/changecp.html',{'user':user,'error' : 'Incorrect Otp','otp':'otp'}, RequestContext(request))
                except :
                    return render_to_response('visitor/changecp.html ',{'user':user,'pass': 'pass'},RequestContext(request))

        if request.POST.get('type') == 'pass':
            password = request.POST.get('password')
            cp = request.POST.get('cp')

            if password != cp:
                return render_to_response('visitor/changecp.html ',{'user':user,'pass': 'pass','error':'Password Dosnot Match'},RequestContext(request))

            else:
                user = request.POST.get('user')
                user = User.objects.get(id = user)
                user.set_password(password)
                user.save()
                user.profile.password = password
                user.profile.save()
                messages.add_message(request,messages.INFO, 'Passwod changed Successfully')
                return HttpResponseRedirect('/user/login/')

    return render_to_response('visitor/changecp.html',{'phone':'phone'},RequestContext(request))


@login_required(login_url = '/user/login/')
def book(request):
    if request.POST:
        by = User.objects.get(id = request.session['userid'])
        appointwith = User.objects.get(id = request.POST.get('with'))
        from datetime import datetime
        on = datetime.strptime(request.POST.get('date'),'%d/%m/%Y').date()
        if Appointment.objects.filter(user=by , appointmentwith = appointwith, on = on).exists():
            return HttpResponseRedirect('/user/')
        spec = request.POST.get('spec')
        time = datetime.strptime(request.POST.get('time'),'%H:%M:%S').time()
        comment = request.POST.get('comment')
        try : 
            service = request.POST.get('service')
        except :
            service = ''

        app = Appointment()
        app.user = by
        app.appointmentwith = appointwith
        app.on = on
        app.specialization = spec
        app.service = service
        app.comment = comment
        app.time = time
        app.save()
        import thread
        thread.start_new_thread(bookingsms,(app.id,))
        thread.start_new_thread(bookingmail,(app.id,))

        return HttpResponse('Appontment Booked Succesfully .<a href="/user/">Go Home </a>')
        


    user = User.objects.get(id = request.GET.get('id'))
    spec = user.answerby.filter(question__title = "Specialization")[0].answer.split('\r\n')
    try :
        service = user.answerby.filter(question__title = "Services And Facilites")[0].answer.split('\r\n')
    except:
        service = ''

    ######### next 7 days of avalibility ########
    date = ast.literal_eval(user.answerby.filter(Q(question__title__icontains = "slot") or Q(question__title__icontains = "timing"))[0].answer)
    days = [x['Day'][:2].lower() for x in date]
    days = getweeklist(days)
    count = 0
    week = 0
    import datetime
    today = datetime.date.today()
    appoint = [] 
    while count < 7 :
        for x in days:
            if today + datetime.timedelta(days=-today.weekday() + x ,weeks=week) >= today:
                appoint.append((today + datetime.timedelta(days=-today.weekday() + x ,weeks=week)).strftime('%d/%m/%Y'))
                count +=1 
        week += 1
    ###### end next 7 days of avalibility ########
    
    context = {
        'spec' : spec,
        'service' : service,
        'date': appoint,
        'id' : request.GET.get('id'),
    }
    return render_to_response('visitor/book.html',context,RequestContext(request))

@login_required(login_url = '/user/login/')
def rate(request):
    if request.is_ajax():
        val = request.POST.get('value')
        print val
        by = User.objects.get(id = request.session['userid'])
        of = User.objects.get(id = request.POST.get('id'))
        if not Rating.objects.filter(of = of, by= by).exists():
            new_rating = Rating()
            new_rating.amount = val
            new_rating.by = by
            new_rating.of = of
            new_rating.save()
    return HttpResponse('True')

@login_required(login_url = '/user/login/')
def review(request):
    if request.POST:
        text = request.POST.get('review')
        by = User.objects.get(id = request.session['userid'])
        of = User.objects.get(id = request.POST.get('of'))
        if Review.objects.filter(of = of, by = by).exists():
            return HttpResponseRedirect(request.POST.get('url'))
        review = Review()
        review.text = text
        review.of = of
        review.by = by
        review.save()

        return HttpResponseRedirect(request.POST.get('url'))