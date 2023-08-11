from django.contrib import admin

# Register your models here.
from .models import CustomUser, Address, DeactivateUser

admin.site.register(CustomUser)
admin.site.register(Address)
admin.site.register(DeactivateUser)