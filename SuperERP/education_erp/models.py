from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class EducationUser(models.Model):
    email = models.EmailField(unique=True)  # Unique within Education ERP only
    password = models.CharField(max_length=128)  # Hashed password
    erp_role = models.CharField(max_length=50, default='student')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Student(models.Model):
    user = models.ForeignKey(EducationUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
