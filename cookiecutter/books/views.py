from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from cookiecutter.books.exceptions import TooManyBooksException, IsCheckedOutException
from cookiecutter.books.logic import Library
from cookiecutter.books.models import Author, Book
from cookiecutter.books.serializers import AuthorSerializer, BookSerializer, CheckoutRequestSerializer, \
    BookDetailSerializer, ReturnBooksRequestSerializer
from cookiecutter.users.models import AppUser


class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.order_by('name')
    serializer_class = AuthorSerializer
    search_fields = ('name',)


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.order_by('title')
    filterset_fields = ('author',)
    search_fields = ('title',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookDetailSerializer

        return BookSerializer

    @action(detail=False, methods=['POST'])
    def checkout_books(self, request):
        serializer = CheckoutRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(AppUser, id=serializer.validated_data.get('user_id'))
        books = []
        for book_id in serializer.validated_data.get('book_ids'):
            book = get_object_or_404(Book, id=book_id)
            books.append(book)

        try:
            Library.checkout_books(user=user, books=books)
        except TooManyBooksException:
            return Response(
                data='This user already has three books checked out or is trying to check out more than three books',
                status=status.HTTP_400_BAD_REQUEST
            )
        except IsCheckedOutException:
            return Response(
                data='One of the books is already checked out.',
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data='Checkout successful.', status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def return_books(self, request):
        serializer = ReturnBooksRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        books = []
        for book_id in serializer.validated_data.get('book_ids'):
            book = get_object_or_404(Book, id=book_id)
            books.append(book)

        Library.return_books(books=books)

        return Response(data='Return successful.', status=status.HTTP_200_OK)
