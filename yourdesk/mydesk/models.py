from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class MailId(models.Model):
    mail_id = models.EmailField()
    otp = models.IntegerField(null=True)

    class Meta:
        db_table = "mail_id"

class User(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mail_id = models.OneToOneField(MailId, on_delete=models.CASCADE)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = "User"

class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    start_date = models.DateField()
    end_date = models.DateField()
    overall_progress = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])

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
