from django.contrib import admin
from .models import Book, User, Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre')
    search_fields = ('title', 'author', 'genre')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('username',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rating')
    list_filter = ('rating',)
    search_fields = ('book__title', 'user__username')
