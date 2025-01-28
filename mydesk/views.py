
from django.views import View
from mydesk.models import User, MailId, Project,Task
from django.http.response import JsonResponse
from mydesk.utils.utils_otp import sendMail
import json
from Accounts.tokenauthentication import JWTAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .pagination import CommentPagination

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

        # project = Project.objects.get(id = project_id)

        # name = project.name
        # description = project.description
        # start_date = project.start_date
        # end_date = project.end_date
        # users = list(project.users.all())
        # try:  
        #     tasks = project.task_set.all().values('name', 'status')
        #     tasks = list(tasks)
        # except:
        #     pass

        # dict_data = {
        #     'name' : name,
        #     'description' : description,
        #     'start_date' : start_date,
        #     'end_date' : end_date,
        #     'tasks' : tasks,
        #     'users' :users
        # }

        # return JsonResponse(dict_data, status = 200)
        project = Project.objects.get(id=project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=200)

    def put(self, request, project_id):
        project = Project.objects.get(id=project_id)
        serializer = ProjectSerializer(project, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Data has been Updated"}, status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)

class tasksView(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        # data = json.loads(request.body)
        # project_id = data.get('project_id')
        # project = Project.objects.get(id = project_id)
        # task = Task(name = data.get('name'),
        #             description = data.get('description'),
        #             due_date = data.get('due_date'),
        #             assigned_date = data.get('assigned_date'),
        #             status = data.get('status'),
        #             project = project)
        # task.save()

        # return JsonResponse({"msg":"task created"}, status = 201)
        serializer = TaskSerializer(data = request.data, partial = True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=HTTP_400_BAD_REQUEST)
        
    def get(self, request, id):

        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, id):

        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=HTTP_400_BAD_REQUEST)
        
class CommentView(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, id):
        #we will use pagination for comments bcoz may be there will lots of comment
        task = Task.objects.get(id = id)
        comments = task.comments.all()
        paginator = CommentPagination()
        paginated_comments = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(paginated_comments, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=HTTP_400_BAD_REQUEST)