#pip install pygraphviz --install-option="--include-path=/usr/local/include/graphviz/" --install-option="--library-path=/usr/local/lib/graphviz"
class Book:

    def add_book(self, edition, isbn, plot, price):
        self.edition = edition
        self.isbn = isbn
        self.plot = plot
        self.price = price
        self.author = Author()


class Author:


    def add_author(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name