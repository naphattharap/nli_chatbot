#!/usr/bin/env python
__author__ = "Naphatthara P."
__version__ = "1.0.0"
__email__ = "naphatthara.p@gmail.com"
__status__ = "Prototype"

from ext_client.google_client import GoogleBookApiService

googleBook = GoogleBookApiService() 
googleBook.google_book_by_title_intent("Harry Potter", 5)
googleBook.google_book_by_genre_intent("Fiction", 5)
googleBook.google_book_by_author_intent("Rowling", 5)
