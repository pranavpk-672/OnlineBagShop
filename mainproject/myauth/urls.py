from django.urls import path
from myauth import views


from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('log/',views.log,name='log'),
    path('home/',views.home,name='home'),

    #forget pass
    #path('request-reset-email/',views.RequestResetEmailView.as_view(),name="request-reset-email"),
    #path("set-new-password/<uidb64>/<token>",views.SetNewPassword.as_view(),name="set-new-password"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete')
    

]