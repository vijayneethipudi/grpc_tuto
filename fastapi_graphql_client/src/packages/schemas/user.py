from typing import List, Optional

import grpc
import strawberry

from packages.protos import users_pb2, users_pb2_grpc


@strawberry.type
class User:
    id: str
    name: str
    email: str


@strawberry.input
class UserInput:
    name: str
    email: str


def get_stub():
    channel = grpc.insecure_channel("localhost:50051")
    return users_pb2_grpc.UsersStub(channel)


# pylint: disable=no-member
@strawberry.type
class UserQuery:
    @strawberry.field
    def users(self) -> List[User]:
        stub = get_stub()
        response = stub.GetUsers(users_pb2.GetUsersRequest())
        return [User(id=user.id, name=user.name, email=user.email) for user in response.users]

    @strawberry.field
    def user(self, id: str) -> Optional[User]:
        stub = get_stub()
        user = stub.GetUserById(users_pb2.GetUserByIdRequest(id=id)).user
        return User(id=user.id, name=user.name, email=user.email)


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, payload: UserInput) -> User:
        stub = get_stub()
        res = stub.CreateUser(
            users_pb2.CreateUserRequest(user=users_pb2.UserMessage(name=payload.name, email=payload.email))
        )
        u = res.user
        return User(id=u.id, name=u.name, email=u.email)

    @strawberry.mutation
    def update_user(self, id: str, payload: UserInput) -> User:
        stub = get_stub()
        res = stub.UpdateUser(
            users_pb2.UpdateUserRequest(user=users_pb2.UserMessage(id=id, name=payload.name, email=payload.email))
        )
        u = res.user
        return User(id=u.id, name=u.name, email=u.email)

    @strawberry.mutation
    def delete_user(self, id: str) -> User:
        stub = get_stub()
        return stub.DeleteUser(users_pb2.DeleteUserRequest(id=id)).user
