from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from packages.schemas.main import schema

app = FastAPI()

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def main():
    return "Welcome to graphql api"
