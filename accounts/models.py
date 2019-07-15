from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.core.mail import send_mail


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields): # username can be missed
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        # @GMAIL.CoM or @gmail.com
        user = self.model(
            email=self.normalize_email(email),
            username = username, # can be missed
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password): #username can be missed
        """
        Creates and saves a superuser with the given email and password.
        """

        user = self.create_user(email, username, password) # username can be missed
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead username"""
    # Username added Optional Can be missed
    username = models.CharField(
                max_length=120,
                validators=[
                    RegexValidator(
                        regex=USERNAME_REGEX,
                        message='Username must be alphanumeric',
                        code='invalid_username'
                        )],
                unique=True,
                )
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    name = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255, default='927778')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() # hook the manager

    # by default is username
    USERNAME_FIELD = 'email' # username
    REQUIRED_FIELDS = ['username'] # email THIS FIELD CAN BE MISSED


####### EXTEND USER MODEL #############

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=120, null=True, blank=True)
    #author_email = models.CharField(max_length=220, validators=[validate_author_email, validate_chris], null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            ActivationKey.objects.create(user=instance)
        except:
            pass
    instance.profile.save()

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class ActivationKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = random_string_generator(size=20)
        qs = ActivationKey.objects.filter(key__iexact=self.key)
        if qs.exists():
            self.key = random_string_generator(size=20)
        super(ActivationKey, self).save(*args, **kwargs)

def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
        x = str(instance.user)
        urlul = "http://127.0.0.1:8000/accounts/activate/" + str(instance.key)
        send_mail("1 click activate", urlul, "transaction7em@gmail.com", [x], fail_silently=False)



post_save.connect(post_save_activation_receiver, sender=ActivationKey)





import random
import string
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
