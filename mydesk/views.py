
from django.views import View
from mydesk.models import User, MailId, Project,Task
from django.http.response import JsonResponse
from mydesk.utils.utils_otp import sendMail
import json
from django.forms.models import model_to_dict
from Accounts.tokenauthentication import JWTAuthentication
from django.contrib.auth import authenticate, login, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class UserMail(View):

    def post(self, request):
        #email = request.POST["email"]
        data = json.loads(request.body)
        email_str = data.get('email')
        # email = User.objects.get(email = email)
        status = 200
        try:
            email = MailId.objects.get(email = email_str)
        except MailId.DoesNotExist:
            email = MailId(email = email_str)
            email.save()
            status = 201
        finally:
            otp = sendMail(email)
            email = MailId.objects.get(email = email_str)
            email.otp = otp
            email.save()
            return JsonResponse({"msg" : "otp sent",}, status = status)

class MailOtp(View):

    def post(self, request):
        data = json.loads(request.body)
        _otp = data.get('otp')
        _email = data.get('email')
        print(_email)
        email_obj = MailId.objects.get(email = _email)
        otp = email_obj.otp
        if _otp == otp :
            return JsonResponse({}, status = 200)
        return JsonResponse({}, status = 400)

class UserDetails(View):

    def post(self, request):
        data = json.loads(request.body)
        try:
            email = MailId.objects.get(email = data.get("email"))
        except MailId.DoesNotExist:
            return JsonResponse({"msg":"Mail Id not found in record, pls validated the otp first",}, status = 400)
        
        email = email.email
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        print(email) #here i am getting string
        print(password)
        print(first_name)
        print(last_name)

        User.objects.create_user(
                    email = email,
                    password = password,
                    first_name = first_name,
                    last_name = last_name
                    )
        
        return JsonResponse({"msg":"User saved to record"}, status = 201)
    
class UserLogin(View):

    def post(self, request):

        data = json.loads(request.body)
        # try:
        #     email = MailId.objects.get(email = data.get("email")) 
        # except MailId.DoesNotExist:
        #     return JsonResponse({"msg":"Mail Id not found in record",}, status = 400)
        
        try:
            user = User.objects.get(email = data.get("email"))
        except user.DoesNotExist:
            return JsonResponse({"msg":"User not found in record, pls register first",}, status = 400)

        _password = data.get("password")

        print(user.email)
        print(_password)

        _email = user.email

        # user = authenticate(username = _email, password = _password)
        login(request=request, user=user)
        print (user)

        if user is not None:
            # login(request=request, user=user)
            token = JWTAuthentication.generate_token(data)
            return JsonResponse({"msg":"Password Validated",
                                 "token":str(token)}, status = 200)

        else:
            return JsonResponse({"msg":"incorrect password"}, status = 401)


class ProjectView(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

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

class tasksView(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

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

        
