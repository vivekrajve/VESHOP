from datetime import datetime

from django.db import models


# Create your models here.
class UserRegister1(models.Model):
    user_type = 'user'
    user_name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=10)
    Street = models.CharField(max_length=100)
    House = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Pin = models.IntegerField()
    Country = models.CharField(max_length=50)
    profile_pic = models.FileField( null=True, blank=True , default='img/profile/default_profile.jpg')


class ShopEmployeeRegister1(models.Model):
    user_type = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=10)
    licence = models.FileField()
    psp  = models.FileField()
    status = models.CharField(max_length=20, default='Pending')
    profile_pic = models.FileField()

class add_category(models.Model):
    category_name = models.CharField(max_length=100)

class product(models.Model):
    p_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.FileField(upload_to='img/product/', null=True, blank=True)
    offer = models.IntegerField()
    price = models.IntegerField()
    quantity = models.IntegerField()

class user_cart(models.Model):
    product_details = models.ForeignKey(product, on_delete=models.CASCADE)
    user_details = models.ForeignKey(UserRegister1, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=1)
    status = models.CharField(max_length=20)

class wishlist(models.Model):
    product_details=models.ForeignKey(product, on_delete=models.CASCADE)
    user_details=models.ForeignKey(UserRegister1, on_delete=models.CASCADE)



class order_details(models.Model):
    user_details = models.ForeignKey(UserRegister1, on_delete=models.CASCADE)
    product_details = models.CharField(max_length=20)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    payment_status = models.CharField(max_length=20,default='NOT PAID')
    delivery_status = models.CharField(max_length=20,default='pending')
    employee_register = models.CharField(max_length=20,default='abc')
    address = models.CharField(max_length=200, default='NIL')
    address_city = models.CharField(max_length=20)
    address_district = models.CharField(max_length=20)
    address_state = models.CharField(max_length=20)
    address_pincode = models.IntegerField(default=0)

class Admin_one(models.Model):
    admin_name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=10)
    profile_pic = models.FileField(null=True, blank=True, )

class Paid_Product(models.Model):
    product_details = models.ForeignKey(product, on_delete=models.CASCADE)
    user_details = models.ForeignKey(UserRegister1, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return (self.product_details.price * self.quantity)


class Message(models.Model):
    user = models.ForeignKey(UserRegister1, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField()
    reply = models.TextField(default="We will get back to you..")
    status = models.TextField(default="0")
    timestamp = models.DateTimeField(default=datetime.now)



class Advertisements(models.Model):
    image = models.FileField(upload_to='img/product/', null=True, blank=True)
    p_name = models.CharField(max_length=100)
    heading = models.CharField(max_length=100)
    subheading = models.CharField(max_length=100)



