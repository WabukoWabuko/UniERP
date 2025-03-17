from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class EducationUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    erp_role = models.CharField(max_length=50, default='student')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Student(models.Model):
    user = models.ForeignKey(EducationUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)  # e.g., "STU001"
    grade = models.CharField(max_length=10)  # e.g., "10A"
    enrollment_date = models.DateField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)
