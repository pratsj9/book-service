from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.db import get_db, engine

from db.model.BookEntity import BookEntity

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db)]


@router.get("/v1/books",summary="Retrieve all the books",status_code=200,
            tags=["books"])
async def get_all_books(db: SessionDep):
    """
    Return all the available books from the database
    :return:
    """
    print("Retrieving all books")
    return db.query(BookEntity).all()


@router.get("/v1/books/{id}",summary="Retrieve a Book by its ID",
            status_code=200 , responses={404 : {"description": "Book ID not found"}},  tags=["books"])
async def get_book_by_id(id:int , db: SessionDep) -> BookEntity:
    """
    Return a book based on the given ID
    :return:
    """
    print(f"Retrieving Book details for given id : {id}")
    book = (db.query(BookEntity)
            .filter(BookEntity.id == id).first())
    return book


@router.post("/v1/books", summary="Create a new Book entry",
            status_code=201 ,  tags=["book-service"])
async def create_book(book_data:BookEntity , db: SessionDep) -> BookEntity:
    """
    Create a new Book Entry in the database
    :param db:
    :param book_data:
    :param payload:
    :return: BookEntity
    """
    print(f"Creating a book entry for {book_data}")
    db.add(book_data)
    db.commit()
    db.refresh(book_data)
    return book_data




@router.put("/v1/books/{id}" , summary="Update a Book entry based on the given Id",
            status_code=200 , responses={404 : {"description": "Given Book Id not found"}}, tags=["books"])
async def update_book(id: int , book_entry: BookEntity) -> BookEntity:
    """
    Update a Book entry based on the given ID
    :param book_data:
    :param id:
    :param payload:
    :return:
    """
    print(f"Updating the book entry for the given id {id}")
    with Session(engine) as session:
        book_session = session.get(BookEntity, id)
        if not book_session:
            raise HTTPException(status_code=404)
        book_data = book_entry.model_dump(exclude_unset=True)
        book_session.sqlmodel_update(book_data)
        session.add(book_session)
        session.commit()
        return book_data


@router.delete("/v1/books/{id}" , summary="Delete a Book entry based on the given Id",
               status_code=204 , responses={404 : {"description": "Given Book Id not found"}}, tags=["books"])
async def delete_book(id: int):
    """
    Delete a Book entry based on the given Id
    :param id:
    :return:
    """
    with Session(engine) as session:
        book_session = session.get(BookEntity, id)
        if not book_session:
            raise HTTPException(status_code=404)
        session.delete(book_session)
        session.commit()
        return {"Book Entry Deleted": "ok"}



