# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'books'
        unique_together = (('title', 'author', 'genre'),)


class Reviews(models.Model):
    book = models.ForeignKey(Books, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'
        unique_together = (('book', 'user'),)


class Users(models.Model):
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'users'
