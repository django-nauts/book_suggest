from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [IsAuthenticated]

	# Filtering by genre
    def get_queryset(self):
        genre = self.request.query_params.get('genre')
        if genre:
            return Book.objects.filter(genre=genre)
        return Book.objects.all()


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [IsAuthenticated]


class AddReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateReviewView(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_object(self):
        book_id = self.kwargs['book_id']
        user_id = self.request.user.id
        return get_object_or_404(Review, book_id=book_id, user_id=user_id)


class DeleteReviewView(generics.DestroyAPIView):
    queryset = Review.objects.all()

    def get_object(self):
        book_id = self.kwargs['book_id']
        user_id = self.request.user.id
        return get_object_or_404(Review, book_id=book_id, user_id=user_id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
