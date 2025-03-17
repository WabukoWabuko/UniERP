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
    staff_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=50)
    hire_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Timetable(models.Model):
    user = models.ForeignKey(EducationUser, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    day_of_week = models.CharField(max_length=10)  # e.g., "Monday"
    start_time = models.TimeField()
    end_time = models.TimeField()

class Fee(models.Model):
    user = models.ForeignKey(EducationUser, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
