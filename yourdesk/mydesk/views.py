from django.shortcuts import render
from django.views import View
from models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

# Create your views here.
class UserMail(View):
    def mailValidator(self, mail_id):
        print("pls validate email")
        return JsonResponse(mail_id, status=201)

    def POST(self, request):
        mail_id = request.POST["mail_id"]
        try:
            User.objects.filter(mail_id = mail_id)
            return JsonResponse(mail_id, status = 200)
        except ObjectDoesNotExist:
            self.mailValidator(mail_id)

class MailOtp(View):
    pass