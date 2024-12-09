from django.shortcuts import render
from django.views import View
from mydesk.models import User, MailId
from django.http.response import JsonResponse
from mydesk.utils.utils_otp import sendMail
import json

# Create your views here.
class UserMail(View):

    def post(self, request):
        #mail_id = request.POST["mail_id"]
        data = json.loads(request.body)
        mail_id = data.get('mail_id')
        status = 200
        try:
            email = MailId.objects.get(mail_id = mail_id)

            #sending 200 for logi
        except MailId.DoesNotExist:
            email = MailId(mail_id = mail_id)
            email.save()
            status = 201
        finally:
            otp = sendMail(mail_id)
            email = MailId.objects.get(mail_id = mail_id)
            email.otp = otp
            email.save()
            return JsonResponse({"msg" : "otp sent",}, status = status)

class MailOtp(View):

    def post(self, request):
        data = json.loads(request.body)
        _otp = data.get('otp')
        mail_id = data.get('mail_id')
        mail_id = MailId.objects.get(mail_id = mail_id)
        otp = mail_id.otp
        if _otp == otp :
            return JsonResponse({}, status = 200)
        return JsonResponse({}, status = 400)

class UserDetails(View):

    def post(self, request):
        data = json.loads(request.body)
        try:
            mail_id = MailId.objects.get(mail_id = data.get("mail_id"))
        except MailId.DoesNotExist:
            return JsonResponse({"msg":"Mail Id not found in record",}, status = 400)
        user = User(first_name = data.get("first_name"),
                    last_name = data.get("last_name"),
                    password = data.get("password"),
                    mail_id = mail_id)
        user.save()

        return JsonResponse({"msg":"User saved to record"}, status = 201)
    
class UserLogin(View):

    def post(self, request):
        data = json.loads(request.body)
        try:
            mail_id = MailId.objects.get(mail_id = data.get("mail_id"))
        except MailId.DoesNotExist:
            return JsonResponse({"msg":"Mail Id not found in record",}, status = 400)
        
        _password = data.get("password")
        password = User.objects.get(mail_id = mail_id).password

        if _password == password:
            return JsonResponse({"msg":"Password Validated"}, status = 200)
        return JsonResponse({"msg":"incorrect password"}, status = 401)
