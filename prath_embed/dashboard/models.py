from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL

# Create your models here.

class UserProfile(AbstractUser):
    # -------UserAdmin Table Fields-------
    SUPERADMIN = 1
    COMPANY = 2
    STUDENT = 3
    PARTNER = 4
    PROGRAMS = 5
    SALES = 6
    ROLE_CHOICES = (
        (SUPERADMIN, 'Super Admin'),
        (COMPANY, 'Company'),
        # (STUDENT, 'Student'),
        # (PARTNER, 'Partner'),
        # (PROGRAMS, 'Program'),
        # (SALES,'Sales')
        )

    email = models.EmailField('email address', unique=True)  # changes email to unique and blank to false
    # first_name = models.CharField(null=True, max_length=100)
    user_role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=COMPANY, blank=True)
    company_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    company_image = models.FileField(upload_to='images')
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.username


class Devices(models.Model):
    device_name = models.CharField(max_length=100)
    device_unique_id = models.CharField(max_length=100)
    company_id =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.device_unique_id)

class Report(models.Model):
    created_at = models.DateTimeField(default=timezone.now, null=True)
    date_field = models.DateField()
    time_field = models.TimeField()
    device_id =  models.ForeignKey(Devices, on_delete=models.CASCADE)
    parameter1 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter2 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter3 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter4 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter5 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter6 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter7 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter8 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter9 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter10 = models.DecimalField(max_digits=5, decimal_places=4)

    def __str__(self):
        return str(self.device_id)

class ProgrammableParameters(models.Model):
    created_at = models.DateTimeField(default=timezone.now, null=True)
    device_id =  models.ForeignKey(Devices, on_delete=models.CASCADE)
    pparameter1 = models.DecimalField(max_digits=5, decimal_places=4)
    pparameter2 = models.DecimalField(max_digits=5, decimal_places=4)
    pparameter3 = models.DecimalField(max_digits=5, decimal_places=4)
    parameter4 = models.DecimalField(max_digits=5, decimal_places=4)
    pparameter5 = models.DecimalField(max_digits=5, decimal_places=4)

    def __str__(self):
        return str(self.device_id)