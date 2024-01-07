from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
import uuid
from django.utils import timezone

# Create your models here.

class UserData(AbstractUser):
    username = None
    name = models.CharField(max_length=100, unique=True,null=True,blank=True)
    email = models.EmailField(max_length=100, unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class UserToken(models.Model):
    user = models.ForeignKey(UserData,on_delete=models.CASCADE,null=True,blank=True)
    token = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    used = models.BooleanField(default=False)

    
    def mark_as_used(self):
        self.used = True
        self.save()