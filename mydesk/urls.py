from django.urls import path
from mydesk.views import UserMail, MailOtp, UserDetails, UserLogin, ProjectView, tasksView

urlpatterns = [
    path("validate-mail/", UserMail.as_view()),
    path("validate-otp/", MailOtp.as_view()),
    path("signup/", UserDetails.as_view()),
    path("login/", UserLogin.as_view()),
    path("project/create/", ProjectView.as_view(), name = "project-create"),
    path("project/<int:project_id>/", ProjectView.as_view(), name = "project-view"),
    path("project/task/create/", tasksView.as_view()),
    path("project/task/<int:id>/", tasksView.as_view()),
]