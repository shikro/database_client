import sys


class book:
    def __init__(self, book_id, name):
        self.id = book_id
        self.name = name
        self.authors = []
        self.genres = []
