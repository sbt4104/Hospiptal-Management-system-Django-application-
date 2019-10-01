from django.db import models
from django.contrib.auth.models import User

desig=(
    ('doctor','doctor'),
    ('patient','patient')
)

# Create your models here.
Choices=(
    ('OPD','OPD'),
    ('orthopedia','orthopedia'),
    ('Pediatric','Pediatric'),
    ('Cardiologist','Cardiologist'),
    ('Gyanecologist','Gyanecologist'),
)
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    contact =  models.CharField(max_length=10)
    designation = models.CharField(default='doctor',max_length=10)
    field = models.CharField(choices=Choices,default='inprocess',max_length=30)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username


# Create your models here.
class UserProfileInfo2(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    contact =  models.CharField(max_length=10)
    designation = models.CharField(default='patient',max_length=10)    
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
