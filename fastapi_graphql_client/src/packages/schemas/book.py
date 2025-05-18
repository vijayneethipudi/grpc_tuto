import typing

import strawberry


def get_books():
    return [Book(title="The great Gatsby", author="JFK")]


@strawberry.type
class Book:
    title: str
    author: str


@strawberry.type
class BookQuery:
    books: typing.List[Book] = strawberry.field(resolver=get_books)
