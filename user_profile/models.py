from datetime import datetime, timezone, timedelta
from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from enum import Enum


from core.models import TimeStampedModel
from core.handle_images import compress_image

from .managers import CustomUserManager

class UserTypes(Enum):
    VENDOR = "VENDOR"
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    return "users/{0}/{1}".format(instance.user.username, filename)


def national_image_path(instance, filename):
    return f"national/{instance.user.username}/images/{filename}"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_MALE = "m"
    GENDER_FEMALE = "f"
    OTHER = "o"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (OTHER, "Other"),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    about = models.TextField(blank=True, null=True)
    trxn_id = models.CharField(max_length=50, null=True, blank=True)

    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True)
    user_type = models.CharField(
        max_length=8,
        choices=[(type.name, type.value) for type in UserTypes],
        default=UserTypes.VENDOR.value,
    )
    otp = models.IntegerField(null=True,blank=True,default=999999)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    @property
    def last_seen(self):
        return cache.get(f"seen_{self.user.username}")


    @property
    def online(self):
        if self.last_seen:
            now = datetime.now(timezone.utc)
            if now > self.last_seen + timedelta(minutes=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs,):
        return super(CustomUser, self).save(*args, **kwargs)


class Address(models.Model):
    # Address options
    BILLING = 'B'
    SHIPPING = 'S'

    ADDRESS_CHOICES = ((BILLING, _('billing')), (SHIPPING, _('shipping')))

    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)

    country = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    primary = models.BooleanField(default=False)
    building_number = models.IntegerField(blank=True, null=True)
    apartment_number = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f"{self.user.get_full_name()}, {self.address_line1}, {self.city}, {self.country}"


class DeactivateUser(TimeStampedModel):
    # user = models.OneToOneField(
    #     User, related_name="deactivate", on_delete=models.CASCADE
    # )
    deactive = models.BooleanField(default=True)


class hide_db_for_registration(models.Model):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
    )
    phone_number = models.CharField(max_length=255,null=True,blank=True)
    username = models.CharField(max_length=255,null=True,blank=True)
    otp = models.IntegerField(null=True,blank=True,default=999999)