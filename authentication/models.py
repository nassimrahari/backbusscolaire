from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    PARENT = 'PARENT'
    ECOLE = 'ECOLE'

    ROLE_CHOICES = (
        (PARENT, 'Parent'),
        (ECOLE, 'Ecole'),
    )
    
    profile_photo = models.ImageField(verbose_name='Photo de profil', null=True, blank=True)
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')

    def __str__(self):
        return self.email
