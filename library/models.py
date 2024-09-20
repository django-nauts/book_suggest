from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)

    class Meta:
        db_table = 'books'
        unique_together = ('title', 'author', 'genre')

    def __str__(self):
        return f'{self.title} by {self.author}'


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        db_table = 'reviews'
        unique_together = ('book', 'user')

    def __str__(self):
        return f'{self.user} rated {self.book} - {self.rating}/5'
