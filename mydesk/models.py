from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class MailId(models.Model):
    email = models.EmailField()
    otp = models.IntegerField(null=True)

    class Meta:
        db_table = "mail_id"

class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    start_date = models.DateField()
    end_date = models.DateField()
    overall_progress = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    users = models.ManyToManyField(User, related_name="projects")

    class Meta:
        db_table = "Projects"
        
class Task(models.Model):

    class Status(models.TextChoices):
        NOT_ASSIGNED = "NA"
        NOT_STARTED = "NS"
        IN_PROGRESS = "IP"
        DELAYED = "DELY"
        COMPLETED = "CMP"
        CANCELLED = "CNCL"
        BLOCKED = "BLK"

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    due_date = models.DateField()
    assigned_date = models.DateField()
    status = models.CharField(
        max_length = 4,
        choices = Status.choices,
        default = Status.NOT_STARTED,
    )
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = "Tasks"

class Comment(models.Model):
    content = models.CharField(max_length = 255)
    time_stamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")

class Team(models.Model):

    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = "Teams"

class TeamMember(models.Model):

    class Role(models.TextChoices):
        MANAGER = "MNG"
        SCRUM_MASTER = "SM"
        TEAM_LEAD = "TL"
        ASSOCIATE = "A"
        JR_ASSOCIATE = "JA"

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=3, choices=Role.choices, default=Role.ASSOCIATE)
    Availability = models.BooleanField()

    class Meta:
        db_table = "Team-Members"

class MessageTableUser(models.Model):

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name= "sender_user")
    reciver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name= "reciver_user")
    content = models.TextField()
    time_stamp = models.DateTimeField()

    class Meta:
        db_table = "user-messages"

class MessageTableTeam(models.Model):

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reciver = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    time_stamp = models.DateTimeField()

    class Meta:
        db_table = "team-messages"

class Notification(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    time_stamp = models.DateTimeField()
    status = models.BooleanField()

    class Meta:
        db_table = "notifications"
