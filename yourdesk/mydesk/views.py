from django.shortcuts import render
from django.views import View
from mydesk.models import User, MailId, Project,Task
from django.http.response import JsonResponse
from mydesk.utils.utils_otp import sendMail
import json
from django.core import serializers
from django.forms.models import model_to_dict

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

class ProjectView(View):

    def post(self, request):
        data = json.loads(request.body)

        project = Project(name = data.get('name'),
                          description = data.get('description'),
                          start_date = data.get('start_date'),
                          end_date = data.get('end_date'),
                          overall_progress = 0)
        
        project.save()

        return JsonResponse({"msg":"Peoject created"}, status = 201)
    
    def get(self, request, project_id):

        project = Project.objects.get(id = project_id)

        name = project.name
        description = project.description
        start_date = project.start_date
        end_date = project.end_date
        try:  
            tasks = project.task_set.all().values('name', 'status')
            tasks = list(tasks)
        except:
            pass

        dict_data = {
            'name' : name,
            'description' : description,
            'start_date' : start_date,
            'end_date' : end_date,
            'tasks' : tasks
        }

        return JsonResponse(dict_data, status = 200)

class tasksView(View):

    def post(self, request):
        data = json.loads(request.body)
        project_id = data.get('project_id')
        project = Project.objects.get(id = project_id)
        task = Task(name = data.get('name'),
                    description = data.get('description'),
                    due_date = data.get('due_date'),
                    assigned_date = data.get('assigned_date'),
                    status = data.get('status'),
                    project = project)
        task.save()

        return JsonResponse({"msg":"task created"}, status = 201)
        
    def get(self, request, id):

        task = Task.objects.get(id = id)
        # task = dict(task)
        task = model_to_dict(task)

        return JsonResponse(task, status = 200, safe= False)

        
