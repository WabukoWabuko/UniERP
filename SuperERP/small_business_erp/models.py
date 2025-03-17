from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class BusinessUser(models.Model):
    email = models.EmailField(unique=True)  # Unique within Small Business ERP only
    password = models.CharField(max_length=128)  # Hashed password
    erp_role = models.CharField(max_length=50, default='owner')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Inventory(models.Model):
    user = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
