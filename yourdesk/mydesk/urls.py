from django.urls import path
from mydesk.views import UserMail, MailOtp

urlpatterns = [
    path("validate-mail", UserMail.as_view()),
    path("validate-otp", MailOtp.as_view()),
]