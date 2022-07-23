import email
from multiprocessing import context
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from yaml import serialize
from api.serializers import DeviceSerializer, ReportSerializer

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import  reverse, path, re_path, include, reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib import auth, messages
from django.core.signing import TimestampSigner



from dashboard.models import Report, Devices, UserProfile

import requests


# Create your views here.

def company_register(request):
    print("inside company_register ")
    if request.method == "POST":
        print("inside if - ", request.POST)
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password=request.POST['password']
        email_id=request.POST['email_id']
        company_name=request.POST['company_name']
        company_address=request.POST['company_address']
        company_image=request.FILES['company_image']

        password=request.POST['password']
        

#Company Login page view
def company_login(request):

    """Login a company if the credentials are valid and the user is active, user is student
    else redirects to the same page and displays an error message."""
    if request.method == "POST":

        print("inside if - ", request.POST)
        username=request.POST['username']
        password=request.POST['password']
        print(username)
        user = authenticate(username=username, password=password)

        if user is not None:
            print("logged in user is not None")


            if user.is_active:
                login(request, user)
                print("logged in")
                role = request.user.user_role
                return HttpResponseRedirect(reverse('dashboard:company_dashboard'))

        else:
            print("logged in user is  None")
            return render(request, 'company_login.html',{'error_message': 'Enter valid details!'})
    else:
        print("inside else - ", request)
        return render(request,'company_login.html')
        # return render(request,'company_login.html')

@login_required(login_url = '/company_login')
def company_dashboard(request):
    """It is company profile page. This page displays after successful login
    of company user in portal which contains Device list """
    email = request.user.email
    company_user = UserProfile.objects.get(email=email)
    print("company_user -", company_user.email)


    device_list = Devices.objects.filter(company_id = company_user.pk)
    print("device_list -", device_list)

    data={
        'company_user':company_user,
        'device_list':device_list
    }
    return render(request,'company_dashboard.html',data)


@login_required(login_url = '/company_login')
def device_report(request,pk):
    """It is company's device report page. This page displays after user selects a device to read and check all parameters """
    print( "device primary key ", pk)
    email = request.user.email
    company_data = UserProfile.objects.get(email=email)
    print("company_data -", company_data.email)

    device_data = Devices.objects.get(pk = pk)
    print("device_data -", device_data)

    device_readings = Report.objects.filter(device_id = pk)
    print("device_readings - ", device_readings)
    
    data={
        'company_data':company_data,
        'device_data':device_data,
        'device_readings': device_readings
    }
    return render(request,'report.html',data)

#Student Logout view
def company_logout(request):
    """Logout User  from the portal"""
    logout(request)
    return HttpResponseRedirect(reverse('dashboard:company_login'))



def company_forgot_password(request):

    return render(request, 'company_forgot_password.html')


# """ password_reset Testing password reset view """
def password_reset(request):
    
    if request.method == "POST":
        print( "inside if ")
        print("password_reset \nrequest.POST ",request.POST)
    else :
        print( "inside else password_reset ")

        return render(request, 'registration/password_reset_form.html') 


    return render(request, 'registration/password_reset_form.html')

def password_reset_done(request):
    
    if request.method == "POST":
        
        print("password_reset_done: \nrequest.POST ",request.POST,flush=True)
        email = request.POST.get('email_id')
        print("username - ",email,flush=True)
        flag = 0
        try :
            company_user = UserProfile.objects.get(email = email)
        except UserProfile.DoesNotExist:
            flag = 1
            print("Company user with email id -",email," does not exist, returning to the password_reset page",flush=True)

        if flag:
            return render(request, 'registration/password_reset_form.html')    
        print("company_user.email- ",company_user.email,flush=True)
        
        
        signer = TimestampSigner()
        value = signer.sign(company_user.email)
        print("value - ",value,flush=True)
        token = signer.unsign(value, max_age=10)
        print("token - ",token,flush=True)
        
        # reset_link = "http://127.0.0.1:8000/online/password_reset_test/"+value
        # base_url = "{0}://{1}".format(request.scheme, request.get_host())
        base_url = "https://enrollment.jaroeducation.com"
        
        reset_link = base_url+"/online/password_reset_test/"+value
        company__email = company_user.email
        print("company__email - ",company__email,flush=True)
        context = {"token":value}

        # email password reset link to student 
        
        toemail_id = company_user.email
        fromemail_id = "noreply@jaro.in"
        # update to your dynamic template id from the UI
        TEMPLATE_ID = 'd-ea97ddb8355840f3ba5aca1932ebdb31'
        # create Mail object and populate
        message = Mail( fromemail_id, toemail_id)
        # pass custom values for our HTML placeholders
        message.dynamic_template_data = {
            'company__email': company__email,
            'reset_link': reset_link,
            # 'event': 'Twilio Signal'
        }
        message.template_id = TEMPLATE_ID
        # create our sendgrid client object, pass it our key, then send and return our response objects
        try:
            sg = SendGridAPIClient(settings.SEND_GRID_API_KEY)
            resp = sg.send(message)
            code, body, headers = resp.status_code, resp.body, resp.headers
            print(f"Response code: {code}",flush=True)
            print(f"Response headers: {headers}",flush=True)
            print(f"Response body: {body}",flush=True)
            print("Dynamic Messages Sent!",flush=True)
        except Exception as e:
            print("Error: {0}".format(e))
    else :
        return render(request, 'registration/password_reset_done.html') 


    return render(request, 'registration/password_reset_done.html', context)
    
    # return HttpResponseRedirect(reverse('jaro_student_portal_app:student_dashboard'))  password_reset_done

def password_reset_test(request,token):
    
    signer = TimestampSigner()
    print("inside password reset test")
    try:
        token = signer.unsign(token, max_age=600)
        print("token",token,flush=True)
        flag = 0
        msg = "Valid link"
        validlink = 1
        
    except : 
        msg = "The password reset link was invalid, possibly because it has already been used. Please request a new password reset."
        flag = 1
        validlink = 0

        
    context = {"msg":msg, "token":token, "validlink":validlink}

    return render(request, 'registration/password_reset_confirm.html',context)

def password_reset_confirm(request):

    print("inside password reset confirm",flush=True)
    print("request.POST",request.POST,flush=True)
    print("password1 - ",request.POST.get("new_password1"),flush=True)
    print("password2 - ",request.POST.get("new_password2"),flush=True)
    candidate_id = request.POST.get("candidate_id")
    new_password1 = request.POST.get("new_password1")
    new_password2 = request.POST.get("new_password2")

    student = UserProfile.objects.get(candidate_id = candidate_id)
    student.password  = make_password(new_password1)
    student.student_password = new_password1
    student.save()
    print("student.password - ",student.password,flush=True)
    print("student.student_password - ",student.student_password,flush=True)


    # ,context
    return render(request, 'registration/password_reset_complete.html')


@login_required(login_url='/company_login/')
def passwordchange(request):

    if request.method == "POST":

        print("inside if",flush=True)
        username = request.user.username
        print("request.user.username - ",request.user.username,flush=True)
        print("password1 - ",request.POST.get("new_password1"),flush=True)
        print("password2 - ",request.POST.get("new_password2"),flush=True)
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        # old_password
        if request.user.student_password != old_password:
            messages.error(request, 'Your old password was entered incorrectly. Please enter it again.')
            return render(request, 'registration/password_change.html')
        elif request.user.student_password == new_password1 or request.user.student_password == new_password2 :
            messages.error(request, 'Old password cannot be new password')
            return render(request, 'registration/password_change.html')
        elif new_password1 != new_password2 :
            messages.error(request, 'The two password fields didn’t match.')
            return render(request, 'registration/password_change.html')
        elif len(new_password1) < 8 or len(new_password2) < 8:
            messages.error(request, 'Your new password must contain at least 8 characters')
            return render(request, 'registration/password_change.html')
        
        else :
            student = UserProfile.objects.get(username = username)
            student.password  = make_password(new_password1)
            student.student_password = new_password1
            student.save()
            logout(request)
            return render(request, 'registration/password_change_done.html')

    else :
        print("inside else",flush=True)
        return render(request, 'registration/password_change.html')