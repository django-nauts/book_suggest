from django.urls import path
from .views import BookListView, BookListView, BookDetailView


urlpatterns = [
	path('api/book/list/', BookListView.as_view(), name='book_list'),
	path("api/book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
]
