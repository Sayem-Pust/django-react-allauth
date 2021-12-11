from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, identifier, password, **kwargs):
        if '@' in identifier:
            user = self.model(identifier=identifier, email=self.normalize_email(identifier), **kwargs)
        else:
            user = self.model(identifier=identifier, phone_number=identifier, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, password, **kwargs):
        user = self.model(
            identifier=identifier,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


roleType = [
    ('USER', 'user'),
    ('SUPPLIER', 'supplier'),
    ('DRIVER', 'driver'),
    ('RESTAURANT', 'restaurant'),
    ('PARTNER', 'partner'),
]


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=255, null=True, blank=True)
    role = models.CharField(choices=roleType, max_length=255)
    is_confirmed = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    identifier = models.CharField(max_length=40, unique=True, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.identifier)


# @receiver(pre_save, sender=User)
# def update_user(sender, instance, **kwargs):
#     user = instance
#     if '@' in user.identifier:
#         email = user.identifier
#         norm_email = email.lower()
#         user.email = norm_email
#     else:
#         user.phone_number = user.identifier


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_details')
    first_name = models.CharField(_('first name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('last'), max_length=255, null=True, blank=True)
    additional_phone_number = models.CharField(_('additional phone number'), max_length=255, null=True, blank=True)

    profile_pic = models.ImageField(upload_to='photos/profile_pic/%Y/%m/%d/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)
    instance.user_details.save()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userDetails.save()


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')

    road = models.CharField(max_length=255, blank=True, null=True)
    suburb = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
