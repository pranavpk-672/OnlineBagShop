
# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        CUSTOMER="CUSTOMER",'Customer'
        DELIVERYBOY="DELIVERYBOY",'deliveryboy'
        SELLER="SELLER",'Seller'


    role = models.CharField(max_length=50,choices=Role.choices)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone = models.CharField(max_length=12, unique=True)  # You can adjust the max_length as needed
    alt_phone = models.CharField(max_length=12, unique=True)  # You can adjust the max_length as needed
    pincode= models.CharField(max_length=6, unique=True)  # You can adjust the max_length as needed
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    building_name = models.CharField(max_length=100)
    road_area = models.CharField(max_length=100)



    def _str_(self):
        return self.user.username
    


    #model for seller
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)  # Set the phone field as unique
    alt_phone = models.CharField(max_length=12, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    gst = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode= models.CharField(max_length=6)  # You can adjust the max_length as needed
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    
    def _str_(self):
        return self.user.first_name
    



#model for product
class Product(models.Model):
    # Product Information Fields
    product_name = models.CharField(max_length=255)
    stock = models.IntegerField()
    about_product = models.TextField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    capacity = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    material = models.CharField(max_length=255)

    # Product Images and Certificate Fields
    image1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # You can add more image fields here if needed
    authentication_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)

    # Other fields and methods for your model as needed

    def __str__(self):
        return self.product_name

    
    