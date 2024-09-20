from django.urls import path
from .views import (
    BookListView, 
    BookDetailView, 
    AddReviewView, 
    UpdateReviewView, 
    DeleteReviewView,
	SuggestBookView,
)


urlpatterns = [
	path('api/book/list/', BookListView.as_view(), name='book_list'),
	path("api/book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),

    path('api/review/add/', AddReviewView.as_view(), name='add_review'),
    path('api/review/update/<int:book_id>/', UpdateReviewView.as_view(), name='update_review'),
    path('api/review/delete/<int:book_id>/', DeleteReviewView.as_view(), name='delete_review'),

	path('api/suggest/', SuggestBookView.as_view(), name='suggest_books'),
]
