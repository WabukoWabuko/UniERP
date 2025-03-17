from django.db import models
from django.contrib.auth.models import User

class BusinessUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)  # No DB constraint
    erp_role = models.CharField(max_length=50, default='owner')

class Inventory(models.Model):
    user = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
