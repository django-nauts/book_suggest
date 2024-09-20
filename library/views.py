from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import Book
from .serializers import BookSerializer


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
