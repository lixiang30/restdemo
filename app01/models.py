from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField()
    pub_date = models.DateField()
    publish = models.ForeignKey("Publish")
    authors = models.ManyToManyField("Author")
    def __str__(self):
        return self.title

class Publish(models.Model):
    name = models.CharField(max_length=12)
    email = models.EmailField()
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    def __str__(self):
        return self.name

# class User(models.Model):
#     name = models.CharField(max_length=32)
#     pwd = models.CharField(max_length=32)
class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    type_choice = ((1,"普通用户"),(2,"VIP"),(3,"SVIP"))
    user_type = models.IntegerField(choices=type_choice,default=1)


class Token(models.Model):
    user = models.OneToOneField("User")
    token = models.CharField(max_length=128)
    def __str__(self):
        return self.token
