from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class SoftDeleteManager(models.Manager):
    def save_soft_delete(self):
        self.is_deleted = True
        self.save()
        return True

    def get_soft_delete(self):
        return self.filter(is_deleted=True)

    def get_unsoft_delete(self):
        return self.filter(is_deleted=False)
