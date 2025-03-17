from django.db import models
from django.contrib.auth.models import User

class EducationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    erp_role = models.CharField(max_length=50, default='student')  # e.g., student, teacher

class Student(models.Model):
    user = models.ForeignKey(EducationUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
