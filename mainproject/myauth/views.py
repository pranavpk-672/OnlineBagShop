from django.shortcuts import render, HttpResponse, redirect
from .models import User
from .models import *
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
#activation and deactivation
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.shortcuts import render
from .models import Profile

from .models import SellerProfile
from django.shortcuts import render
from .models import SellerProfile

from .models import Product  # Import your Product model here





class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        super().__init__()  #Call the parent class's __init__ method

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

    return render(request, 'auth/signup.html',)
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
               # messages.success(request,"Login Success")
                #request.session['email']=myuser.email

                #session
                request.session['username']=username




                if myuser.role=='CUSTOMER':
                        #messages.success(request,"Login Sucess!!!")
                        return redirect('home')
                elif myuser.role=='SELLER':
                        #messages.success(request,"Login Sucess!!!")
                        return redirect('seller_dashboard')
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
        items = Product.objects.all()[:12]
        response = render(request,'home.html',{'items': items})
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
      else:
        return redirect('/myauth/login')
        #return render(request,'home.html')


        #sellerlogin
def sellersig(request):
       if 'username' in request.session:
        response = render(request,'sellersign.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
       else:
        return redirect('/myauth/login')

#admin dashboard
def adminreg(request):
    # Query all User objects (using the custom user model) from the database

    
    # Render the HTML template
    return render(request, 'admintemplate.html' )



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


#user view
def adminn(request):
    User = get_user_model()
    user_profiles = User.objects.filter(role='CUSTOMER')
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request,'userview.html',context)

def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    subject = 'Account Activation'
    html_message = render_to_string('activation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return redirect('/myauth/adminn/')

def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse("You cannot deactivat the admin.")
    user.is_active = False
    user.save()
    subject = 'Account Deactivation'
    html_message = render_to_string('deactivation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    # Send an email to the user here
    return redirect('/myauth/adminn/')



#userview2
def userviewss(request):
    # Retrieve customer profiles with the role 'CUSTOMER'
    user_profiles = Profile.objects.filter(user__role='CUSTOMER')
    print(user_profiles)
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request, 'userviews.html', context)




#about
def abouttt(request):

    return render(request, 'about.html' )
#contact
def con(request):

    return render(request, 'contact.html' )
#updateprofilr
def updateprofile(request):
    
   return render(request,'auth/updateprofile.html')


#updateprofile

def update_profile(request):
    if request.method == 'POST':
        # Process the form data and update the user's profile
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        altphone = request.POST['alt_phone']
        img = request.FILES.get('profile_picture')
        pin = request.POST['pincode']
        statee = request.POST['state']
        cityy = request.POST['city']

        housename = request.POST['building_name']
        roadname = request.POST['road_area']
        if User.objects.filter(username=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email is already taken")
            return redirect('update-profile')  # Redirect to the same page with the warning message

        # Validate phone
        if Profile.objects.filter(phone=phone).exclude(user=request.user).exists():
            messages.warning(request, "Phone number is already taken")
            return redirect('update-profile')  # Redirect to the same page with the warning message

        
        
        if email != request.user.email:
            user=request.user
            user.email=email
            user.username=email
            user.is_active=False  #make the user inactive
            user.save()
            
            
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('auth/activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.info(request,"Active your account by clicking the link send to your email")
            logout(request)
           
            return redirect('/myauth/login')
            
        
        # Update the User model fields
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username=email
        user.email = email
        user.save()
        
        # Update the Profile model fields
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = phone
        profile.alt_phone = altphone
        profile.profile_picture = img
        profile.pincode = pin
        profile.state = statee
        profile.city = cityy
        profile.building_name = housename
        profile.road_area = roadname
        profile.save()
        

        # Logout the user and redirect to the signup page
        messages.success(request,'profile updated')
        return redirect('home')
    else:
        return render(request, 'auth/updateprofile.html', {'user': request.user})
    
    #seller signup
def sell(request):
    
    return render(request,'auth/seller_signup.html')



#seller signup
def signupsell(request):
    if request.method == "POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.warning(request, "Password is not matching")
            return render(request, 'auth/seller_signup.html')

        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email is already taken")
                return render(request, 'auth/seller_signup.html')
        except Exception as identifier:
            pass

        myuser = User.objects.create_user(first_name=fname,last_name=lname,email=email,password=password,username=email,role='SELLER')
        print(myuser)

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

    return render(request, 'auth/seller_signup.html')











#update_seller_profile

def seller_profile_update(request):
    if request.method == 'POST':
        # Process the form data and update the user's profile
        # Retrieve form fields
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        altphone = request.POST['alt_phone']
        #img = request.POST['profile_picture']
        img = request.FILES.get('profile_picture')

        gst = request.POST['gst']
        pin = request.POST['pincode']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST.get('address')
        company_name = request.POST.get('company_name')
        country = request.POST.get('country')

        # Check if the email is already taken by another user
        if User.objects.filter(username=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email is already taken")
            return redirect('sell_upd')  # Redirect to the same page with the warning message

        # Validate phone number
        if Profile.objects.filter(phone=phone).exclude(user=request.user).exists():
            messages.warning(request, "Phone number is already taken")
            return redirect('sell_upd')  # Redirect to the same page with the warning message

        # If the email is different from the current user's email, update the email and send an activation email
        if email != request.user.email:
            user = request.user
            user.email = email
            user.username = email
            user.is_active = False  # Make the user inactive
            user.save()
            
            current_site = get_current_site(request)  
            email_subject = "Activate your account"
            message = render_to_string('auth/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            EmailThread(email_message).start()
            messages.info(request, "Activate your account by clicking the link sent to your email")
            logout(request)
            return redirect('/myauth/login')

        # Update the User model fields
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = email
        user.email = email
        user.save()
        
        # Update the SellerProfile model fields
        seller_profile, created = SellerProfile.objects.get_or_create(user=user)
        seller_profile.phone = phone
        seller_profile.alt_phone = altphone
        seller_profile.profile_picture = img
        seller_profile.pincode = pin
        seller_profile.state = state
        seller_profile.city = city
        seller_profile.company_name = company_name
        seller_profile.country = country
        seller_profile.address = address
        seller_profile.gst = gst
        seller_profile.save()

        # Logout the user and redirect to the seller profile update page
        messages.success(request, 'Profile updated  and Approval is pending')
        return redirect('sell_upd')
    else:
        # Render the seller profile update page
        return render(request, 'sellersign.html', {'user': request.user})



#seller view
def sellerr(request):
    User = get_user_model()
    user_profiles = User.objects.filter(role='SELLER')
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request,'seller_view.html',context)

def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    subject = 'Account Activation'
    html_message = render_to_string('activation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return redirect('/myauth/sellerr/')

def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse("You cannot deactivat the admin.")
    user.is_active = False
    user.save()
    subject = 'Account Deactivation'
    html_message = render_to_string('deactivation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    # Send an email to the user here
    return redirect('/myauth/sellerr/')

#sellerview2
def sellviews(request):
    # Retrieve seller profiles with the role 'SELLER'
    user_profiles = SellerProfile.objects.filter(user__role='SELLER')

    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request, 'seller_viewss.html', context)


#seller approval
def sellor_approval(request):
    unapproved_sellers = SellerProfile.objects.filter(is_approved=False)
    
    return render(request,'pending_seller_activation.html',{'unapproved_sellers': unapproved_sellers})



def approve_seller(request, seller_id):
    seller = SellerProfile.objects.get(pk=seller_id)
    seller.is_approved = True
    seller.save()
    subject = 'Your Seller Account Has Been Approved'
    message = 'Dear {},\n\nYour seller account has been approved by the admin. You can now log in and start using your account.\n\nLogin Link: http://127.0.0.1:8000/auth_app/handlelogin/'.format(seller.user.first_name)
    from_email = 'prxnv2832@gmail.com'  # Replace with your email address
    recipient_list = [seller.user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    return redirect('sellor_approval')


#seller approval
def seller_dashboard(request):
    try:
        seller_profile = request.user.sellerprofile
        if seller_profile.is_approved:
            return render(request, 'seller_dashboard.html')
        else:
            messages.success(request, 'Your profile is pending admin approval.')
            return redirect('sellersign')  # Redirect to the sellersign view
    except SellerProfile.DoesNotExist:
        messages.success(request, 'You do not have a seller profile.')
        return redirect('sellersig')




 #seller add product
def selleraddprod(request):
    
    return render(request,'seller_add_prod.html')






def add_product(request):
    if request.method == 'POST':
        # Retrieve data from the form
        stock = request.POST.get('stock')
        capacity = request.POST.get('capacity')
        color = request.POST.get('color')
        material = request.POST.get('material')


        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        product_name = request.POST.get('product_name')
        current_price = request.POST.get('current_price')
        about_product = request.POST.get('about_product')
        # Retrieve images and certificate
        image1 = request.FILES['image1']
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        # Uncomment these lines if you plan to use image4 and authentication_certificate
        # image4 = request.FILES.get('image4')
        authentication_certificate = request.FILES['authentication_certificate']

        # Create a new Product instance and save it
        product = Product(
            category=category,
            sub_category=sub_category,
            product_name=product_name,
            current_price=current_price,
            stock=stock,
            color=color,
            capacity=capacity,
            material=material,
            about_product=about_product,

            image1=image1,
            image2=image2,
            image3=image3,
            # image4=image4,  # Uncomment if needed
             authentication_certificate=authentication_certificate,  # Uncomment if needed
        )

        # Assuming you have a 'seller' field in your Product model to associate the seller
        product.seller = request.user.sellerprofile
        

        product.save()
        messages.success(request, "Product added successfully. Waiting for approval.")
        return redirect('seller_dashboard')
    
    return render(request, 'seller_add_prod.html')


# def index(request):
#     items = Product.objects.all()
#     return render(request, '.html',{'items': items})




#product detailed view
    
def prodetailview(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detailed_view.html', {'product': product})

#ALL product  view
def productallview(request):
    items = Product.objects.all()
    
    return render(request,'product_view.html',{'items': items})

#ALL product  view
def cartt(request):
    
    return render(request,'cart.html')


#Admin view products
def admin_prodview(request):
     products = Product.objects.all()
     return render(request, 'admin_view_product.html', {'products': products})
    








