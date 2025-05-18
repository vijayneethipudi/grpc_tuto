import logging
from concurrent import futures
from uuid import uuid4

import grpc

from packages.db.conn import SessionLocal
from packages.models.user import UserModel
from packages.protos import users_pb2, users_pb2_grpc


# pylint: disable=no-member
class UsersService(users_pb2_grpc.UsersServicer):

    def GetUsers(self, request, context):
        db = SessionLocal()
        users = db.query(UserModel).all()
        return users_pb2.GetUsersResponse(
            users=[users_pb2.UserMessage(id=user.id, name=user.name, email=user.email) for user in users]
        )

    def GetUserById(self, request, context):
        db = SessionLocal()
        user = db.query(UserModel).filter_by(id=request.id).first()
        return users_pb2.GetUserByIdResponse(user=users_pb2.UserMessage(id=user.id, name=user.name, email=user.email))

    def CreateUser(self, request, context):
        db = SessionLocal()
        user = request.user
        new_user = UserModel(id=str(uuid4()), name=user.name, email=user.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return users_pb2.CreateUserResponse(
            user=users_pb2.UserMessage(
                id=new_user.id,
                name=new_user.name,
                email=new_user.email,
            )
        )

    def UpdateUser(self, request, context):
        db = SessionLocal()
        user = db.query(UserModel).filter_by(id=request.user.id).first()
        user.name = request.user.name
        user.email = request.user.email
        db.commit()
        return users_pb2.CreateUserResponse(
            user=users_pb2.UserMessage(
                id=user.id,
                name=user.name,
                email=user.email,
            )
        )

    def DeleteUser(self, request, context):
        db = SessionLocal()
        user = db.query(UserModel).filter_by(id=request.id).first()
        if user:
            db.delete(user)
            db.commit()
            return users_pb2.DeleteUserResponse(
                user=users_pb2.UserMessage(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                )
            )
        return None


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    users_pb2_grpc.add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port("[::]:50051")
    print("Users 2 Service Started at port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
