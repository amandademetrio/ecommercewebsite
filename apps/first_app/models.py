from django.db import models
import re
from django.contrib import messages
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class AdminManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}

        if len(postData['full_name']) < 1:
            errors['full_name_len'] = "Full name can't be empty"
        if len(postData['email']) < 2:
            errors['email_len'] = "Email should have at least 2 characters"
        if len(postData['password']) < 2:
            errors['password_len'] = "Password should have at least 2 characters"

        if not postData['full_name'].isalpha():
            errors['full_name_alpha'] = "Name must contain only letters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Invalid email format"

        if Admin.objects.filter(email=postData['email']):
            errors['already_registered'] = "Email is already in the database"

        if postData['password'] != postData['confirm_password']:
            errors['password_match'] = "Both passwords match"
        return errors
    
    def login_validator(self,postData):
        errors = {}

        if len(postData['email']) < 0:
            errors['email_len_login'] = "Email should have at least 2 characters"
        if len(postData['password']) < 2:
            errors['password_len_login'] = "Password should have at least 2 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format_login'] = "Invalid email format"

        if not Admin.objects.filter(email=postData['email']):
            errors['email_db_check'] = "Invalid credentials"
        else:
            log_user = Admin.objects.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), log_user.password.encode()):
                errors['pw_db_check'] = "Invalid credentials"

        return errors

class Admin(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField()
    objects = AdminManager()

class UserManager(models.Manager):
    def address_validator(self,postData):
        errors = {}

        if len(postData['full_name']) < 1 or len(postData['address']) < 1 or len(postData['city']) < 1 or len(postData['state']) < 1 or len(postData['zipcode']) < 1:
            errors['len_error'] = "You must fill all the fields in the Shipping form"

        return errors

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    full_name = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=300)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=2)
    shipping_zipcode = models.CharField(max_length=5)
    billing_address = models.CharField(max_length=300)
    billing_city = models.CharField(max_length=255)
    billing_state = models.CharField(max_length=2)
    billing_zipcode = models.CharField(max_length=5)
    user_level = models.IntegerField()
    objects = UserManager()

class ProductManager(models.Manager):
    pass

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    name = models.CharField(max_length=255)

class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    name = models.CharField(max_length=255)
    main_picture = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    inventory_count = models.IntegerField()
    sold_count = models.IntegerField()
    price = models.IntegerField()
    objects = ProductManager()
    category = models.ForeignKey(Category, related_name="related_products")
    #Update Jul27
    quantity_in_order = models.IntegerField(default=1)

class OrderStatus(models.Model):
    status = models.CharField(max_length=255)

class PaymentStatus(models.Model):
    status = models.CharField(max_length=255)

class OrderManager(models.Manager):
    pass

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    customer = models.ForeignKey(User, related_name="orders")
    products = models.ManyToManyField(Product, related_name="related_orders")
    order_status = models.ForeignKey(OrderStatus, related_name="related_orders")
    payment_status = models.ForeignKey(PaymentStatus, related_name="related_orders")
    shippment_price = models.IntegerField()
    objects = OrderManager()