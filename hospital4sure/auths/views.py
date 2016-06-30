from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as storage
from django.core.serializers.json import DjangoJSONEncoder
from django.core import management
from auths.management.commands import sendotp
from auths.models import *
import random, string, json, re, urllib2 , urllib, ast
from django.contrib import messages
from django.db.models import Q


# Create your views here.

def comcall(message):
    management.call_command('sendotp',message, verbosity=0)
    print 'message sent'


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
        print cat_id
        for cat in cat_id:
            cat.spec = Question.objects.filter(category = cat).filter(title = 'Specialization')[0].options.split('\r\n')
        context = {
            'cat' : cat_id,
        }
        return render_to_response('anon/index.html',context,RequestContext(request))

    profile = User.objects.get(id = request.session['userid']).profile
    
    if profile.verfied == 0 :
    	return HttpResponse('Your Mobile Number Is not Yet Verified. <a href="/sendotp/">Click Here</a> To verify.')

    if profile.register == 0 :
        return HttpResponseRedirect('/form/')

    return HttpResponseRedirect('/profile/')

def signup(request):
    try:
        del request.session['count']
        del request.session['otp']
        del request.session['change']
    except:
        pass
    return render_to_response('auth/signup.html',RequestContext(request))

def signupprocess(request):
    if request.POST:
        try:
            username = request.POST.get('username')
            isd = request.POST.get('isd')

            if len(username) != 10 :
                error = 'Phone Number should be of 10 Digits'
                return render_to_response('auth/signup.html',{'error' : error},RequestContext(request))

            try :
                print int(username)
            except :
                error = 'Phone Number Only has Digits'
                return render_to_response('auth/signup.html',{'error' : error},RequestContext(request))
            
            if (User.objects.filter(username = isd + username).exists()):
                error = 'Phone Number already Registered Try Login'
                return render_to_response('auth/signup.html',{'error' : error},RequestContext(request))
        except Exception, e:
            print e
            error = 'Phone Number Not Entered'
            return render_to_response('auth/signup.html',{'error' : error},RequestContext(request))
        
        try :
            int(request.POST.get('category'))
            cat = Category.objects.get(id = int(request.POST.get('category')))
            if len(SubCategory.objects.filter(category = cat)) > 0:
                try :
                    sub_cat = SubCategory.objects.get(id = int(request.POST.get('subcat')))
                except:
                    error = 'Please Choose A Sub Category'
                    return render_to_response('auth/signup.html',{'error' : error},RequestContext(request))
        except Exception, e:
            print e
            error = 'Please Choose A Category'
            return render_to_response('auth/signup.html',{'error' : error},RequestContext(request))

        try :
            print request.POST.get('email')
            email = request.POST.get('email')
        except Exception,e :
            error = 'Please Enter A valid Email id'
            return render_to_response('auth/signup.html',{'error' : error},RequestContext(request))

        password = request.POST.get('password')
        cp = request.POST.get('cp')
        
        if cp != password :
            error = 'Password Didnt Match '
            context = {
                'error': error,
            }
            return render_to_response('auth/signup.html',context,RequestContext(request))

        new = User()
        new.username = isd + username
        new.save()
        new.set_password(password)
        new.email = email
        new.save()
        profile = UserProfile()
        profile.user = new
        profile.password = password
        profile.category = cat
        if len(SubCategory.objects.filter(category = cat)) > 0:
            profile.subcategory = sub_cat
        profile.save()

        user = authenticate(username=isd + username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['userid'] = user.id
                print 'logged in'

        return HttpResponseRedirect('/sendotp/')

@login_required(login_url='/login/')
def sendotp(request):
    user = User.objects.get(id = request.session['userid'])
    if 'count' in request.session :
        if request.session['count'] > 3:
            error = 'Please Try Later Your Account is Temporarly Deactivated'
            user.is_active = False
            user.save()
            return render_to_response('auth/verification.html',{'error': error}, RequestContext(request))

    if request.POST:
        if request.POST.get('otp') == request.session['otp'] : 
            user.profile.verfied = 1 
            user.profile.save()
            try:
                del request.session['count']
                del request.session['otp']
                del request.session['change']
            except:
                pass
            return HttpResponseRedirect('/form/')
        else :
            request.session['count'] += 1
        return render_to_response('auth/verification.html', RequestContext(request))

    if 'otp' in request.session:
        return HttpResponse('')

    otp = ''.join(random.choice(string.digits) for i in range(6))
    request.session['otp'] = otp
    request.session['count'] = 1
    request.session['change'] = 1
    print request.session['otp']

    username = user.username
    data = otp + '.' + username

    import thread
    thread.start_new_thread(comcall,(data,))

    return render_to_response('auth/verification.html', RequestContext(request))

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


def category(request):
    if request.is_ajax():
        category = []
        for c in Category.objects.all():
            category.append({'id': c.id, 'name': c.name})
        return HttpResponse(json.dumps({"status": "Success", "message": "Category Data Fetched", "data": category},
                                           cls=DjangoJSONEncoder))

def subcategory(request):
    if request.is_ajax():
        sc = []
        cat = request.GET.get('id')
        subcat = SubCategory.objects.filter(category__id = cat)
        for c in subcat:
            sc.append({'id': c.id, 'name': c.name})
        return HttpResponse(json.dumps({"status": "Success", "message": "Category Data Fetched", "data": sc},
                                           cls=DjangoJSONEncoder))

def test(request):
    user = User.objects.get(username = '+911234567890')
    spec = user.answerby.filter(question__title = "Specialization")[0].answer.split('\r\n')
    return HttpResponse(len(spec))

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

                    if user.profile.verfied == 0 :
                        return HttpResponseRedirect('')
                    if user.profile.register == 0 :
                        return HttpResponseRedirect('/form/')
                    return HttpResponseRedirect('/profile/')
                else:
                    state = "your account is not active"
            else:
                state = 'your username and/or password was wrong'
        else:
            state = 'No such user exists'

        return render_to_response('auth/login.html', {'error': state}, RequestContext(request))
    return render_to_response('auth/login.html', RequestContext(request))


@login_required(login_url='/login/')
def form(request):
    option=[]
    user = User.objects.get(id = request.session['userid'])
    if user.profile.register == 1 :
        return HttpResponseRedirect('/profile/')

    category = user.profile.category
    try:
        subcategory = user.profile.subcategory
        questions = Question.objects.filter(category = category).filter(subcategory = subcategory)
        first = questions.filter(order = 1)[0]
        for ques in questions:
            if len(ques.options) != 0:
                option.append({'id': ques.id,'options' : ques.options.split('\r\n')})
        context = {
                'first' : first,
                'subcat' : subcategory,
                'cat' : category,
                'user' : user,
                'options' :  option,
                'question' : questions,
                'document' : Document.objects.filter(category = category),
            }
        return render_to_response('auth/form.html',context,RequestContext(request))
    except :        
        questions = Question.objects.filter(category = category)
        first = questions.filter(order = 1)[0]
        for ques in questions:
            if len(ques.options) != 0:
                option.append({'id': ques.id,'options' : ques.options.split('\n')})
        context = {
                'first' : first,
                'cat' : category,
                'user' : user,
                'options' :  option,
                'question' : questions,
                'document' : Document.objects.filter(category = category),
            }
        return render_to_response('auth/form.html',context,RequestContext(request))


@login_required(login_url='/login/')
def submit(request):
    if request.POST:
        if 'postcount' not in request.session:
            user = User.objects.get(id = request.session['userid'])
            if user.profile.register == 1:
                return HttpResponseRedirect('/profile/')
            category = user.profile.category
            try:
                subcategory = user.profile.subcategory
                questions = Question.objects.filter(category = category).filter(subcategory = subcategory)
            except Exception, e:
                questions = Question.objects.filter(category = category)

            for ques in questions:
                if ques.type < 3 :
                    if ques.require == 'required':
                        try :
                            ans = request.POST.get(str(ques.id))
                        except :
                            messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                    else:
                        ans = str(request.POST.get(str(ques.id)))
                            
                elif ques.type == 3 :
                    if ques.require == 'required':
                        try :
                            ans = ''
                            listt = request.POST.getlist(str(ques.id))
                            for x in listt:
                                ans = ans + str(x) + '\r\n'
                        except:
                            messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                            
                    else:
                        ans = ''
                        listt = str(request.POST.getlist(str(ques.id)))
                        for x in listt:
                            ans = ans + str(x) + '\r\n'

                elif ques.type == 4 :
                    if ques.require == 'required':
                        try:
                            print listt
                            ans = ''                
                            listt = request.POST.getlist(str(ques.id))
                            for x in listt:
                                try:
                                    y =  x[:len(x)-2] + '%0D%0A'
                                    ans = ans + request.POST.get(y) + ' ' + str(x) + '\r\n'
                                except:
                                    ans = ans + str(request.POST.get(x)) + ' ' + str(x) + '\r\n'
                        except Exception, e:
                            print e
                            messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                            
                    else:
                        try:
                            print listt
                            ans = ''                
                            listt = request.POST.getlist(str(ques.id))
                            for x in listt:
                                try:
                                    y =  x[:len(x)-2] + '%0D%0A'
                                    ans = ans + request.POST.get(y) + ' ' + str(x)+ '\r\n'
                                except:
                                    ans = ans + str(request.POST.get(x)) + ' ' + str(x) +'\r\n'
                        except Exception, e:
                            print e
                            ans = ''                
                            listt = (request.POST.getlist(str(ques.id)))
                            for x in listt:
                                y =  x[:len(x)-2] + '%0D%0A'
                                ans = ans + str(request.POST.get(y)) + ' ' + str(x)+ '\r\n'
                        
                    
                elif ques.type == 5 :
                    if ques.require == 'required':
                        try :
                            ans = request.POST.get(str(ques.id))
                        except :
                            messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                    else:
                        ans = str(request.POST.get(str(ques.id)))

                elif ques.type == 6:
                    if ques.require == 'required':
                        try :
                            ans = request.POST.get(str(ques.id))
                        except :
                            messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                            
                    else:
                        ans = str(request.POST.get(str(ques.id)))

                elif ques.type == 7 :
                    if ques.require == 'required':
                        try:
                            ans = []
                            options = ques.options.split('\n')
                            js = request.POST.getlist(str(ques.id))
                            i = 0                    
                            while(i<len(js)):
                                j = 0
                                ob={}
                                while(j < len(options)):
                                    ob['%s'%options[j]] = js[i]
                                    j=j+1
                                    i=i+1
                                ans.append(ob)
                        except:
                            messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                    else :
                        try:
                            ans = []
                            options = ques.options.split('\r\n')
                            js = (request.POST.getlist(str(ques.id)))
                            i = 0                    
                            while(i<len(js)):
                                j = 0
                                ob={}
                                while(j < len(options)):
                                    ob[options[j]] = js[i]
                                    j=j+1
                                    i=i+1
                                ans.append(ob)
                        except:
                            ans = ''


                new_answer = UserAnswer()           
                new_answer.question = ques
                new_answer.user = user
                new_answer.save()
                new_answer.answer = ans           
                new_answer.save()

            try :
                user.profile.username = request.POST.get('username')
                user.profile.register = 1
                user.profile.telephone = request.POST.get('std') + request.POST.get('tel')

                try:
                    user.profile.website = request.POST.get('website')
                    user.profile.save()
                except Exception, e:
                    user.profile.save()
            except :
                messages.add_message(request,messages.ERROR, ' username already exist')

            add = Address()
            add.user = user
            add.type = 'complete'
            add.state = request.POST.get('state_1')
            add.district = request.POST.get('district_1')
            add.city = request.POST.get('city_1')
            add.street = request.POST.get('street_1')
            add.pincode = request.POST.get('pincode_1')
            try:
                add.landmark = request.POST.get('landmark_1')           
            except Exception, e:
                pass
            add.save()

            if str(request.POST.get('auto')) == 'same':
                add2 = Address()
                add2.user = user
                add2.type = 'postal'
                add2.state = request.POST.get('state_1')
                add2.district = request.POST.get('district_1')
                add2.city = request.POST.get('city_1')
                add2.street = request.POST.get('street_1')
                add2.pincode = request.POST.get('pincode_1')
                try:
                    add2.landmark = request.POST.get('landmark_1')               
                except Exception, e:
                    pass
                add2.save()
            else:
                add2 = Address()
                add2.user = user
                add2.type = 'postal'
                add2.state = request.POST.get('state_2')
                add2.district = request.POST.get('district_2')
                add2.city = request.POST.get('city_2')
                add2.street = request.POST.get('street_2')
                add2.pincode = request.POST.get('pincode_2')
                try:
                    add2.landmark = request.POST.get('landmark_2')               
                except Exception, e:
                    pass
                add2.save()

            document = Document.objects.filter(category = category)
            for docs in document:
                typee = docs.Format.split(',')
                if request.FILES['file_' + str(docs.id)].content_type.lower() in typee:
                    if docs.MaxSize*1024*1024 > request.FILES['file_' + str(docs.id)].size:
                        doc = UserDocument()
                        doc.user = user
                        doc.documnet = docs
                        doc.file = request.FILES['file_' + str(docs.id)]
                        doc.save()
                    else:
                        user.profile.register = 0
                        user.profile.save()
                        messages.add_message(request,messages.ERROR, '%s size limit exceded'%docs )

                else:
                    user.profile.register = 0
                    user.profile.save()
                    messages.add_message(request,messages.ERROR, '%s Invalid File type'%docs )
                
            request.session['postcount'] = 1
            return HttpResponseRedirect('/profile/')

@login_required(login_url='/login/')
def profile(request):
    try:
        del request.session['postcount']
    except:
        pass

    print 'hhh'
    user = User.objects.get(id = request.session['userid'])
    category = user.profile.category
    try:
        subcategory = user.profile.subcategory
        questions = Question.objects.filter(category = category).filter(subcategory = subcategory)
        first = questions.filter(order = 1)[0]
    except :
        questions = Question.objects.filter(category = category)
        first = questions.filter(order = 1)[0]
    first.ans = UserAnswer.objects.filter(question__id = first.id).filter(user = user)[0].answer
    print first.ans,first
    address1 = Address.objects.filter(user = user).filter(type = 'complete')[0]
    address2 = Address.objects.filter(user = user).filter(type = 'postal')[0]
    std = user.profile.telephone[:len(user.profile.telephone)-10]
    num = user.profile.telephone[-10:]
    for  ques in questions:
        if ques.type < 2 or ques.type == 5:
            ques.ans = ques.questionof.filter(user = user)[0].answer

        elif ques.type == 2:
            option = ques.options.split('\r\n')
            ques.ans = ques.questionof.filter(user = user)[0].answer
            print ques.ans
            listt = []
            for op in option:
                if op in ques.ans:
                    print 'hi'
                    a  = {'op': op, 'selected' : 'selected'}
                else:
                    a = {'op': op, 'selected' : ''}
                listt.append(a)
            ques.opt = listt


        elif ques.type == 3:
            options = ques.options.split('\r\n')           
            ques.answer = ques.questionof.filter(user = user)[0].answer.split('\r\n')
            listt = []
            for op in options:
                if op in ques.answer:
                    a  = {'op': op, 'check' : 'checked'}
                else:
                    a = {'op': op, 'check' : ' '}
                listt.append(a)
            ques.opt = listt
            
        elif ques.type == 4:
            options = ques.options.split('\r\n')
            ques.answer = ques.questionof.filter(user = user)[0].answer.split('\r\n')
            answer = []
            optt = {}
            for ans in ques.answer:
                answer.append(ans[ans.find(' ')+1:])
                optt[ans[ans.find(' ')+1:]] = ans[:ans.find(' ')]
            listt = []
            for op in options:
                if op in answer:
                    a  = {'op': op, 'check' : 'checked', 'value': optt[op]}
                else:
                    a  = {'op': op, 'check' : '', 'value': ''}
                listt.append(a)
            ques.opt = listt

        elif ques.type == 6:
            ques.ans = ques.questionof.filter(user = user)[0].answer

        elif ques.type == 7:
            import ast
            ans = []
            ques.ans = ast.literal_eval(ques.questionof.filter(user = user)[0].answer)

        document = UserDocument.objects.filter(user = user)
        upload = []
        for d in document:
            upload.append(d.documnet)
        docs = Document.objects.filter(category = category)
        for doc in docs:
            if doc in upload:
                doc.file = document.filter(documnet = doc)[0].file
            else:
                doc.file = ' '
        
    context = {
        'first' : first,
        'question' : questions,
        'address1' : address1,
        'address2' : address2,
        'profile' : user.profile,
        'document' : docs,
        'std': std,
        'num': num,
    }

    return render_to_response('auth/profile.html',context,RequestContext(request))

@login_required(login_url='/login/')
def edit(request):
    if request.method == "POST":
    
        user = User.objects.get(id = request.session['userid'])
        category = user.profile.category
        try:
            subcategory = user.profile.subcategory
            questions = Question.objects.filter(category = category).filter(subcategory = subcategory)
        except Exception, e:
            questions = Question.objects.filter(category = category)

        for ques in questions:
            if ques.type < 3 :
                if ques.require == 'required':
                    try :
                        ans = request.POST.get(str(ques.id))
                        print ans,'if',ques
                    except :
                        messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                        
                else:
                    ans = str(request.POST.get(str(ques.id)))
                    print ans,'else'
                        
            elif ques.type == 3 :
                if ques.require == 'required':
                    try :
                        ans = ''
                        listt = request.POST.getlist(str(ques.id))
                        for x in listt:
                            ans = ans + str(x) + '\r\n'
                    except:
                        messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                        
                else:
                    ans = ''
                    listt = str(request.POST.getlist(str(ques.id)))
                    for x in listt:
                        ans = ans + str(x)+ '\r\n'

            elif ques.type == 4 :
                if ques.require == 'required':
                    try:
                        ans = ''                
                        listt = request.POST.getlist(str(ques.id))
                        for x in listt:
                            try:
                                ans = ans + request.POST.get(x) + ' ' + str(x)+ '\r\n'
                            except:
                                ans = ans + str(request.POST.get(x)) + ' ' + str(x)+ '\r\n'
                    except Exception, e:
                        print e
                        messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                        
                else:
                    try:
                        ans = ''                
                        listt = request.POST.getlist(str(ques.id))
                        for x in listt:
                            try:
                                ans = ans + request.POST.get(x) + ' ' + str(x) + '\r\n'
                            except:
                                ans = ans + str(request.POST.get(x)) + ' ' + str(x) + '\r\n'
                    except Exception, e:
                        print e
                        ans = ''                
                        listt = (request.POST.getlist(str(ques.id)))
                        for x in listt:
                            ans = ans + str(request.POST.get(x)) + ' ' + str(x) + '\r\n'
                    
                
            elif ques.type == 5 :
                if ques.require == 'required':
                    try :
                        ans = request.POST.get(str(ques.id))
                    except :
                        messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                        
                else:
                    ans = str(request.POST.get(str(ques.id)))

            elif ques.type == 6:
                if ques.require == 'required':
                    try :
                        ans = request.POST.get(str(ques.id))
                    except :
                        messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                        
                else:
                    ans = str(request.POST.get(str(ques.id)))

            elif ques.type == 7 :
                if ques.require == 'required':
                    try:
                        ans = []
                        options = ques.options.split('\n')
                        js = request.POST.getlist(str(ques.id))
                        i = 0                    
                        while(i<len(js)):
                            j = 0
                            ob={}
                            while(j < len(options)):
                                ob['%s'%options[j]] = js[i]
                                j=j+1
                                i=i+1
                            ans.append(ob)
                    except:
                        messages.add_message(request,messages.ERROR, '%s is required' %ques.title)
                        
                else :
                    try:
                        ans = []
                        options = ques.options.split('\r\n')
                        js = (request.POST.getlist(str(ques.id)))
                        i = 0                    
                        while(i<len(js)):
                            j = 0
                            ob={}
                            while(j < len(options)):
                                ob[options[j]] = js[i]
                                j=j+1
                                i=i+1
                            ans.append(ob)
                    except:
                        ans = ''


            new_answer = UserAnswer.objects.filter(question = ques).filter(user = user)[0]           
            new_answer.question = ques
            new_answer.user = user
            new_answer.save()
            new_answer.answer = ans           
            new_answer.save()

        try :
            user.profile.username = request.POST.get('username')
            user.profile.register = 1
            user.profile.telephone = request.POST.get('std') + request.POST.get('tel')

            try:
                user.profile.website = request.POST.get('website')
                user.profile.save()
            except Exception, e:
                user.profile.save()
        except :
            messages.add_message(request,messages.ERROR, 'username already exist')


        add = Address.objects.filter(user = user).filter(type = 'complete')[0]
        add.user = user
        add.type = 'complete'
        add.state = request.POST.get('state_1')
        add.district = request.POST.get('district_1')
        add.city = request.POST.get('city_1')
        add.street = request.POST.get('street_1')
        add.pincode = request.POST.get('pincode_1')
        try:
            add.landmark = request.POST.get('landmark_1')           
        except Exception, e:
            pass
        add.save()

        if str(request.POST.get('auto')) == 'same':
            add2 = Address.objects.filter(user = user).filter(type = 'postal')[0]
            add2.user = user
            add2.type = 'postal'
            add2.state = request.POST.get('state_1')
            add2.district = request.POST.get('district_1')
            add2.city = request.POST.get('city_1')
            add2.street = request.POST.get('street_1')
            add2.pincode = request.POST.get('pincode_1')
            try:
                add2.landmark = request.POST.get('landmark_1')               
            except Exception, e:
                pass
            add2.save()
        else:
            add2 = Address.objects.filter(user = user).filter(type = 'postal')[0]
            add2.user = user
            add2.type = 'postal'
            add2.state = request.POST.get('state_2')
            add2.district = request.POST.get('district_2')
            add2.city = request.POST.get('city_2')
            add2.street = request.POST.get('street_2')
            add2.pincode = request.POST.get('pincode_2')
            try:
                add2.landmark = request.POST.get('landmark_2')               
            except Exception, e:
                pass
            add2.save()

        document = Document.objects.filter(category = category)
        for docs in document:
            typee = docs.Format.split(',')
            try :
                if request.FILES['file_'+ str(docs.id)].content_type.lower() in typee:
                    if docs.MaxSize*1024*1024 > request.FILES['file_'+ str(docs.id)].size:
                        doc = UserDocument.objects.filter(user = user).filter(documnet = docs)[0]
                        doc.user = user
                        doc.documnet = docs
                        doc.file = request.FILES['file_'+ str(docs.id)]
                        doc.save()
                    else:
                        user.profile.register = 0
                        user.profile.save()
                        messages.add_message(request,messages.ERROR, '%s size limit exceded' %docs.name)
                else:
                    user.profile.register = 0
                    user.profile.save()
                    messages.add_message(request,messages.ERROR, '%s Invalid File type' %docs.name)
            except Exception, e:
                print e

        return HttpResponseRedirect('/profile/')

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
                
                return render_to_response('auth/changecp.html',{'otp':'otp', 'user': user.id},RequestContext(request))
                

            except Exception, e:
                print e
                return render_to_response('auth/changecp.html',{'phone':'phone', 'error' : 'Phone Nunmber Does Not Exist'},RequestContext(request))
        
        if request.POST.get('type') == 'otp':
            user = request.POST.get('user')    
            if 'count' in request.session :
                if request.session['count'] > 3:
                    return render_to_response('auth/changecp.html',{'user':user,'error' : 'Failed to verify 3 times Contact Site Admin','otp':'otp'}, RequestContext(request))

            if request.POST:
                try : 
                    if request.POST.get('otp') == request.session['otp']: 
                        try:
                            del request.session['count']
                            del request.session['otp']
                            del request.session['change']
                        except:
                            pass
                        return render_to_response('auth/changecp.html ',{'user':user,'pass': 'pass'},RequestContext(request))
                    else :
                        request.session['count'] += 1
                        return render_to_response('auth/changecp.html',{'user':user,'error' : 'Incorrect Otp','otp':'otp'}, RequestContext(request))
                except :
                    return render_to_response('auth/changecp.html ',{'user':user,'pass': 'pass'},RequestContext(request))

        if request.POST.get('type') == 'pass':
            password = request.POST.get('password')
            cp = request.POST.get('cp')

            if password != cp:
                return render_to_response('auth/changecp.html ',{'user':user,'pass': 'pass','error':'Password Dosnot Match'},RequestContext(request))

            else:
                user = request.POST.get('user')
                user = User.objects.get(id = user)
                user.set_password(password)
                user.save()
                user.profile.password = password
                user.profile.save()
                messages.add_message(request,messages.INFO, 'Passwod changed Successfully')
                return HttpResponseRedirect('/login/')

    return render_to_response('auth/changecp.html',{'phone':'phone'},RequestContext(request))

def getcities(request):
    if request.is_ajax():
        q = request.GET.get('term', False)
        results = []
        name_json = ''
        listt = Address.objects.filter(Q(city__icontains=q)).filter(type = 'complete')
        print listt
        for city in listt:
            name_json = city.city.lower()
            if name_json in results:
                pass
            else:
                results.append(name_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def getlocal(request):
    if request.is_ajax():
        city = request.GET.get('city')
        q = request.GET.get('term', False)
        results = []
        name_json = ''
        listt = Address.objects.filter(city__iexact = city).filter(type = 'complete').filter(Q(landmark__istartswith=q))
        print city,listt
        for landmark in listt:
            name_json = landmark.landmark.lower()
            if name_json in results:
                pass
            else:
                results.append(name_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def getspec(request):
    if request.is_ajax():
        cat = request.GET.get('cat')
        q = request.GET.get('term', False)
        results = []
        name_json = ''
        listt = Question.objects.filter(category = cat).filter(title = 'Specialization')[0].options.split('\r\n')
        print listt
        for val in listt:
            print q
            if(val.lower().find(q.lower()) != -1):
                name_json = val
                results.append(name_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def search(request):
    if request.POST:
        spec = ''
        city = request.POST.get('city')
        landmark = request.POST.get('locality')
        cat = request.POST.get('category')
        print cat

        if landmark != '' :
            user = User.objects.filter(profile__category = cat)
            user = user.filter(address__city__iexact = city,address__landmark__iexact = landmark,address__type = 'complete')
        else:
            user = User.objects.filter(profile__category = cat)
            user = user.filter(address__city__iexact = city,address__type = 'complete')

        if request.POST.get('specialization') != '':
            spec = request.POST.get('specialization')            
            user = user.filter(Q(answerby__answer__icontains = spec), answerby__question__title = 'Specialization')
             

        for usr in user:
            usr.add = usr.address.filter(type='complete')[0]
            usr.name = usr.answerby.filter(question__order = 1)[0].answer
            usr.spec = usr.answerby.filter(question__title = "Specialization")[0].answer.split('\r\n')
            doc = Document.objects.filter(category = cat, list_view = 1)[0]
            usr.doc = usr.docsof.filter(documnet = doc)[0].file 
                       
        context = {
            'users' : user,
            'city': city,
            'locality' : landmark,
            'selcat' : cat,
            'cat' : Category.objects.all(),
            'spec' : spec,
            'catname' : Category.objects.get(id = cat),
        }
        return render_to_response('anon/list.html',context,RequestContext(request))


def viewprofile(request,category_name,username):
    user = User.objects.get(profile__username = username)
    answer = UserAnswer.objects.filter(user = user)[:17]
    for x in answer:
        x.disp = [s.name for s in x.question.disp.all()]
        if x.question.type == 3 or x.question.type == 4 :
            x.opt = x.answer.split('\r\n')
        elif x.question.type == 7:
            x.answer = ast.literal_eval(x.answer)
            chek = x.answer[0]
            op = x.question.options.split('\r\n')[0]
            if chek[op] == "":
                x.answer = ''

    user.add = user.address.filter(type='complete')[0]
    user.name = user.answerby.filter(question__order = 1)[0].answer
    user.fb = user.answerby.filter(question__title = "FaceBook Page Link")[0].answer
    doc = Document.objects.filter(category__name = category_name , list_view = 1)[0]
    user.doc = user.docsof.filter(documnet = doc)[0].file
    user.file = user.docsof.filter(user = user, documnet__Format__icontains = 'image')[:4]
    user.location = user.answerby.filter(question__title = "Locate On Map")[0].answer
    context = {
            'usr' : user,
            'catname' : category_name,
            'cat' : Category.objects.all(),
            'answers' : answer,
    }
    return render_to_response('anon/profile.html',context,RequestContext(request))


def searchlink(request,category_name,spec):
    if request.POST:
        print request.POST.get('city')
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['specialization'] = spec
        request.POST['locality'] = ''
        request.POST['category'] = category_name
        mutable = False
        request.POST._mutable = mutable
        return search(request)