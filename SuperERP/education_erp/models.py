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
    student_id = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10)
    enrollment_date = models.DateField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)

class Staff(models.Model):
    user = models.ForeignKey(EducationUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=20, unique=True)  # e.g., "STF001"
    role = models.CharField(max_length=50)  # e.g., "Teacher", "Admin"
    hire_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Monthly salary
