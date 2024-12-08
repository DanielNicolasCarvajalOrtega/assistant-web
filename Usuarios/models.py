from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    rol = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class UserRol(models.Model):
    rol = models.CharField(max_length=50)
    rol_name = models.CharField(max_length=100)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
