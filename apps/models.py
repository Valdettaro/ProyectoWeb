from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  #implementa la hora en la que se crea el mensaje, necesita importar libreria

    def __str__(self):
        return self.name

class Materiales(models.Model):
    material = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.material

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Rating(models.Model):
    rating = models.PositiveIntegerField(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 11)], default=1)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.rating} Stars'