from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    userphone = models.CharField(db_column='userphone', max_length=30)
    userrole = models.CharField(db_column='userrole', max_length=10, default="student")
