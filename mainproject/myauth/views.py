from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.generic import View

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.encoding import DjangoUnicodeDecodeError
import re
from django.core.mail import EmailMessage

from django.views.generic import View
from django.core.mail import EmailMessage


#from .utils import *
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
# getting token from utils.py
from .utils import TokenGenerator,generate_token
#emails
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
#threading
import threading

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        super().__init__()  # Call the parent class's __init__ method

    def run(self):
        self.email_message.send()
 

# Create your views here.

def signup(request):
    if request.method == "POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.warning(request, "Password is not matching")
            return render(request, 'auth/signup.html')

        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email is already taken")
                return render(request, 'auth/signup.html')
        except Exception as identifier:
            pass

        myuser = User.objects.create_user(first_name=fname,last_name=lname,email=email,password=password,username=email,role='CUSTOMER')

        #authentication
        myuser.is_active=False

        myuser.save()
        #authentication
        current_site=get_current_site(request)
        email_subject="Activate your Account"
        message=render_to_string('auth/activate.html',{
             'User':myuser,
             'domain':'127.0.0.1:8000',
             'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
             'token':generate_token.make_token(myuser)
             
        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        




        messages.info(request, " Activate your account by clicking link on your email")
        return redirect('/myauth/login')

    return render(request, 'auth/signup.html')
#login
def handlelogin(request):
    if request.method=="POST":
        username=request.POST['email']
        userpassword=request.POST['password']
        myuser=authenticate(username=username,password=userpassword)

       # if myuser is not None:
          #  login(request,myuser)
         #   #messages.success(request,"Login Success")
        #    return render(request,'index.html')
       # else:
      #      messages.error(request,"Invalid credential")
     #       return redirect('/myauth/login')
    #return render(request,'auth/login.html')


        if myuser is not None:
                login(request,myuser)
                #request.session['email']=myuser.email

                #session
                request.session['username']=username




                if myuser.role=='CUSTOMER':
                        #messages.success(request,"Login Sucess!!!")
                        return redirect('home')
                elif myuser.role=='DELIVERYBOY':
                        messages.success(request,"Login Sucess!!!")
                        return HttpResponse("seller login")
                elif myuser.role=='ADMIN':
                          
                          return redirect('adminreg')
                          
        else:
                messages.error(request,"Invalid credential")
                return redirect('/myauth/login')
    #return render(request,'auth/login.html')

   #session
    response = render(request,'auth/login.html')
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response


#delivery signup
def log(request):
    
    return render(request,'auth/log.html')



#logout
def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/myauth/login')


login_required
def home(request):
      
      if 'username' in request.session:
        response = render(request,'home.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
      else:
        return redirect('/myauth/login')
        #return render(request,'home.html')

#admin dashboard
def adminreg(request):
    # Query all User objects (using the custom user model) from the database
    User = get_user_model()
    user_profiles = User.objects.filter(role='CUSTOMER')
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    
    # Render the HTML template
    return render(request, 'admin.html', context)


#authentication
class ActivateAccountView(View):
     def get(self,request,uidb64,token):
          try:
               uid=force_bytes(urlsafe_base64_decode(uidb64))
               myuser=User.objects.get(pk=uid)
          except Exception as identifier:
               myuser=None
          if myuser is not None and generate_token.check_token(myuser,token):
               myuser.is_active=True
               myuser.save()
               messages.info(request,"Account Activated Successfully")
               return redirect('/myauth/login')
          return render(request,'auth/activatefail.html')     

