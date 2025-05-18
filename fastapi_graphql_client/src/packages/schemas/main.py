import strawberry

from packages.schemas.book import BookQuery
from packages.schemas.student import StudentQuery
from packages.schemas.user import UserMutation, UserQuery


@strawberry.type
class Query(BookQuery, StudentQuery, UserQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
