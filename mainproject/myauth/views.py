
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

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
        myuser.save()
        messages.info(request, "Signup success, please login")
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
                          messages.success(request,"Login Sucess!!!")
                          return HttpResponse("Admin login ")
                          
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
