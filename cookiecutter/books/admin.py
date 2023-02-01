from django.contrib import admin
from django.contrib.admin import ModelAdmin

from cookiecutter.books.models import Book, Author


class AuthorAdmin(ModelAdmin):
    list_display = ('name',)


class BookAdmin(ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
