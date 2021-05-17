from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] ="First name must be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] ="Last name must be more than 2 characters"
        if not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = "Invalid email address!"
        users_with_email=User.objects.filter(email= postData['email'])
        if len(users_with_email) >=1:
            errors['duplicate']="Email already exists!"
        if len(postData['password']) < 5:
            errors['password'] ="Password needs to be more than 5 characters"
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        return errors

class ParkManager(models.Manager):
    def park_validator(self, postData):
        errors = {}
        parks_in_db=Park.objects.filter(park_name= postData['park_name'])
        if len(parks_in_db) >=1:
            errors['duplicate']="Park already exists!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Park(models.Model):
    park_name= models.CharField(max_length=255)
    location= models.CharField(max_length= 255)
    description= models.TextField()
    image=models.ImageField(upload_to=None, height_field=None, width_field=None,max_length=100)
    fee=models.IntegerField(blank=True, null=True)
    users_favorited = models.ManyToManyField(User, related_name="parks")
    objects= ParkManager()