from django.urls import path
from mydesk.views import UserMail, MailOtp, UserDetails, UserLogin, ProjectView, tasksView, CommentView

urlpatterns = [
    path("api/validate-mail/", UserMail.as_view()),
    path("api/validate-otp/", MailOtp.as_view()),
    path("api/signup/", UserDetails.as_view()),
    path("api/login/", UserLogin.as_view()),
    path("api/project/create/", ProjectView.as_view(), name = "project-create"),
    path("api/project/<int:project_id>/", ProjectView.as_view(), name = "project-view"),
    path("project/task/create/", tasksView.as_view()),
    path("project/task/<int:id>/", tasksView.as_view()),
    path("api/comment/<int:id>/", CommentView.as_view()),
    path("api/comment/create/", CommentView.as_view())
]