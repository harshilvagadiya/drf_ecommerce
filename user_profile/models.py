from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    return "users/{0}/{1}".format(instance.user.username, filename)


def national_image_path(instance, filename):
    return f"national/{instance.user.username}/images/{filename}"


class CustomUser(AbstractUser):
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

    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


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
    
    def save(self, *args, **kwargs):
        # phone_number = self.phone_number
        # link = f'https://staging.equipp.in/show_varify/{phone_number}'
        # self.varification_info = link
        return super(CustomUser, self).save()


class Address(models.Model):
    # Address options
    BILLING = 'B'
    SHIPPING = 'S'

    ADDRESS_CHOICES = ((BILLING, _('billing')), (SHIPPING, _('shipping')))
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    
    country = models.CharField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    primary = models.BooleanField(default=False)
    phone_number = models.CharField(null=True, blank=True)
    building_number = models.IntegerField(blank=True, null=True)
    apartment_number = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f"{self.user.get_full_name()}, {self.address_line1}, {self.city}, {self.country}"
    

