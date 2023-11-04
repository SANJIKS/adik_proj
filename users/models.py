from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Укажите email!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    inn = models.CharField(max_length=100)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, 
        choices=[(i / 10, f"{i / 10}") for i in range(10, 51, 5)],  
        default=5
    )
    total_rating = models.DecimalField(max_digits=6, decimal_places=1, default=0.0)  
    rating_votes = models.PositiveIntegerField(default=0)
    is_contractor = models.BooleanField(default=False)

    password_reset_code = models.CharField(max_length=6, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff
    

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.email