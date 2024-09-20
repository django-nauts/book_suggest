from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


from .models import Book, Review, User
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


class SuggestBookView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        # Get the username from query parameters or request data
        username = request.query_params.get('username')

        if not username:
            return Response({"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the user from the custom User model based on the provided username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has any reviews
        user_reviews = Review.objects.filter(user=user)
        if not user_reviews.exists():
            return Response({"message": "there is not enough data about you"}, status=status.HTTP_404_NOT_FOUND)

        # Find the user's highest-rated genre
        top_genre = (
            user_reviews
            .values('book__genre')
            .annotate(avg_rating=Avg('rating'))
            .order_by('-avg_rating')
            .first()
        )

        if not top_genre:
            return Response({"message": "there is not enough data about you"}, status=status.HTTP_404_NOT_FOUND)

        # Get books from the top genre that the user hasn't reviewed yet
        recommended_books = Book.objects.filter(genre=top_genre['book__genre']).exclude(id__in=user_reviews.values('book_id'))

        if not recommended_books.exists():
            return Response({"message": "No more books to suggest from your favorite genre."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the recommended books
        serializer = self.get_serializer(recommended_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
