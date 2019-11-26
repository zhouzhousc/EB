from django.db import models

from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


# Create your models here.

class User(AbstractUser, BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'gateway_user'
        verbose_name = '网关用户'
        verbose_name_plural = verbose_name

