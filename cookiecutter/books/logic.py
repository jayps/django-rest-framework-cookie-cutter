from datetime import datetime, timedelta
from typing import List

from cookiecutter.books.exceptions import TooManyBooksException, IsCheckedOutException
from cookiecutter.books.models import Book
from cookiecutter.users.models import AppUser


class Library:
    @staticmethod
    def checkout_books(user: AppUser, books: List[Book]):
        # Some cool logic here.

        # Users can't check out more than three books at a time.
        if user.loaned_books.count() >= 3 or user.loaned_books.count() + len(books) > 3:
            raise TooManyBooksException

        # Check that all the books are avaialble
        checked_out_books = [book for book in books if book.is_checked_out]
        if len(checked_out_books) > 0:
            raise IsCheckedOutException

        # Checkout the books for the user. Also set their due date two weeks in the future.
        for book in books:
            book.is_checked_out = True
            book.on_loan_to = user
            book.due_date = datetime.now() + timedelta(weeks=2)
            book.save()

    @staticmethod
    def return_books(books: List[Book]):
        for book in books:
            book.is_checked_out = False
            book.on_loan_to = None
            book.save()
