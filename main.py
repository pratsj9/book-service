from fastapi import FastAPI
from sqlmodel import SQLModel

from db.db import engine
from api.v1.books import router

app = FastAPI()


app.include_router(router)

@app.get("/ping")
async def root():
    return {"The Book Service says Pong!"}


@app.on_event("startup")
async def initialize_db():
    create_db_and_tables()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)