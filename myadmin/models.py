from django.db import models

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    catname=models.CharField(max_length=50,unique=True)
    caticon=models.CharField(max_length=100)

class SubCategory(models.Model):
    subcatid=models.AutoField(primary_key=True)
    subcatname=models.CharField(max_length=50,unique=True)
    catname=models.CharField(max_length=50)
    subcaticon=models.CharField(max_length=100)

class Addproduct(models.Model):
    pid=models.AutoField(primary_key=True)
    atitle=models.CharField(max_length=50)
    acategory=models.CharField(max_length=50)
    adescription=models.CharField(max_length=100)
    baseprice=models.CharField(max_length=50)
    info=models.CharField(max_length=50)