from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class EducationUser(AbstractUser):
    erp_role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('student', 'Student')])
    permissions = models.JSONField(default=dict)  # Custom permissions e.g., {"view_students": true, "edit_fees": false}

    def __str__(self):
        return self.email

class Student(models.Model):
    user = models.OneToOneField(EducationUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    enrollment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(EducationUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=50)
    hire_date = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=12.0)
    leave_balance = models.IntegerField(default=20)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    user = models.ForeignKey(EducationUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.date}"

class Fee(models.Model):
    user = models.ForeignKey(EducationUser, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - ${self.amount}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField()

    def __str__(self):
        return self.title

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"
