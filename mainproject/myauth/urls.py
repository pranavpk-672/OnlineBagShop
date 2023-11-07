from django.contrib.auth.base_user import AbstractBaseUser
from django.urls import path
from myauth import views


from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

from django.conf import settings
from django.conf.urls.static import static

 


urlpatterns = [

    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('log/',views.log,name='log'),
    path('home/',views.home,name='home'),
    path('adminreg/',views.adminreg,name='adminreg'),
    path('adminn/',views.adminn,name='adminn'),
    path('abouttt/',views.abouttt,name='abouttt'),
    path('con/',views.con,name='con'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    path('update-profile/',views.update_profile,name='update-profile'),
    path('sell/',views.sell,name='sell'),
    path('signupsell/',views.signupsell,name='signupsell'),
    path('sellersig/',views.sellersig,name='sellersig'),
    path('sell_upd/',views.seller_profile_update,name='sell_upd'),

    path('sellerr/',views.sellerr,name='sellerr'),
    path('sellviews/',views.sellviews,name='sellviews'),
    path('userviewss/',views.userviewss,name='userviewss'),


    #selleer approval
    path('sellor_approval/',views.sellor_approval,name="sellor_approval"),
    path('approve_seller/<int:seller_id>/', views.approve_seller, name='approve_seller'),
    path('seller_dashboard/',views.seller_dashboard,name='seller_dashboard'),

    path('selleraddprod/',views.selleraddprod,name='selleraddprod'),
    path('add_product/',views.add_product,name='add_product'),




#product detailed view
path('prodetailview/<int:product_id>/', views.prodetailview, name='prodetailview'),
   # path('products/<int:product_id>/', views.product_detail, name='product_detail'),


# ALL product view
path('productallview/', views.productallview, name='productallview'),
path('cartt/', views.cartt, name='cartt'),
path('admin_prodview/', views.admin_prodview, name='admin_prodview'),











#activate and  deactivate
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),




    #forget pass
    #path('request-reset-email/',views.RequestResetEmailView.as_view(),name="request-reset-email"),
    #path("set-new-password/<uidb64>/<token>",views.SetNewPassword.as_view(),name="set-new-password"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    

    #authentication

    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate')

]

#image
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)