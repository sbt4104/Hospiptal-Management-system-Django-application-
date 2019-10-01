from django.db import models
from account.models import UserProfileInfo2, UserProfileInfo
# Create your models here.
Choices1 = (
    ('Sunday','Sunday'),
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday'),
)
class Schedules(models.Model):
    user = models.ForeignKey(UserProfileInfo, related_name='doc', on_delete=models.CASCADE)
    avlday = models.CharField(choices = Choices1, default='monday', max_length=20)
    avltime = models.TimeField()
    status = models.IntegerField(default=0)

Choices2=(
    ('inprocess','inprocess'),
    ('accepted','accepted'),
    ('complete','complete'),
)
class Case(models.Model):
    patient =  models.ForeignKey(UserProfileInfo2, related_name='doctors', on_delete=models.CASCADE)
    appointday = models.CharField(choices = Choices1, default='monday', max_length=20)
    appointtime = models.TimeField()
    status = models.CharField(choices=Choices2,default='inprocess',max_length=30)
    doctor = models.ForeignKey(UserProfileInfo, related_name='doctors', on_delete=models.CASCADE)
    prescription = models.TextField(default='please provide prescription', max_length=500)   