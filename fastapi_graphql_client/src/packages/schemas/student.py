from typing import List

import strawberry


@strawberry.type
class Student:
    name: str
    age: int


def get_students():
    return [
        Student(name="Alice", age=21),
        Student(name="Bob", age=23),
    ]


@strawberry.type
class StudentQuery:
    students: List[Student] = strawberry.field(resolver=get_students)
