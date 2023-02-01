from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from cookiecutter.books.models import Book, Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "title",
            "author"
        )


class BookDetailSerializer(ModelSerializer):
    author = AuthorSerializer(many=False)

    class Meta:
        model = Book
        fields = (
            "title",
            "author"
        )


class CheckoutRequestSerializezr(Serializer):
    user_id = serializers.UUIDField()
    book_ids = serializers.ListField(
        child=serializers.UUIDField()
    )
