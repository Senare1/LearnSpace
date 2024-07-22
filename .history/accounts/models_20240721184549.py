from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from .constants import *

class CustomUserManager(BaseUserManager):
    def create_user(self, learner_email, learner_level=None, password=None, **extra_fields):
        """Create and return a regular user with an email and learner level."""
        if not learner_email:
            raise ValueError("Email is required")
        learner_email = self.normalize_email(learner_email)
        
        is_first_cycle = False
        if learner_level in dict(FIRST_CYCLE).keys():
            is_first_cycle = True
        
        user = self.model(learner_email=learner_email, learner_level=learner_level, is_first_cycle=is_first_cycle, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, learner_email, password=None, **extra_fields):
        """Create and return a superuser with an email."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(learner_email, password=password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model that extends AbstractBaseUser and PermissionsMixin."""
    learner_phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    learner_phone = models.CharField(validators=[learner_phone_regex], max_length=16, unique=True, verbose_name="Telephone", blank=True, null=True)
    learner_email = models.EmailField(unique=True, verbose_name="Email", blank=True, null=True)
    learner_level = models.CharField(max_length=128, choices=LEARNER_LEVEL, verbose_name="Classe", blank=True, null=True)
    is_first_cycle = models.BooleanField(default=False)
    teacher_register = models.CharField(max_length=32, verbose_name="Matricule", unique=True, blank=True, null=True)
    teacher_matter = models.ForeignKey('courses.Matter', on_delete=models.CASCADE, related_name="teachers", blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_learner = models.BooleanField(default=True)
    learner_subscription = models.CharField(max_length=12, choices=LEARNER_SUBCRIPTION, default="STANDARD", blank=True, null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "learner_email"

    def __str__(self):
        return self.learner_email

class UserProgress(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.learner_email} - {self.progress}%"
