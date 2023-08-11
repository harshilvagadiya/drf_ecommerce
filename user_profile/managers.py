from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number=None, password=None, user_type=None, **extra_fields):
        
        if not password:
            raise ValueError("-------User must have a password-------")
        if not phone_number:
            raise ValueError("-------User must have a phone number-------")

        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.user_type = user_type
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number=None, password=None, user_type=None, **extra_fields):
        user = self.create_user(phone_number=phone_number, password=password, user_type = "ADMIN", **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
        
