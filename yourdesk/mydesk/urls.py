from django.urls import path
from mydesk.views import UserMail, MailOtp, UserDetails, UserLogin

urlpatterns = [
    path("validate-mail", UserMail.as_view()),
    path("validate-otp", MailOtp.as_view()),
    path("signup", UserDetails.as_view()),
    path("login", UserLogin.as_view()),
]