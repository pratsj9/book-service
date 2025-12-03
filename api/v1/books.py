from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.db import get_db

from db.model.BookEntity import BookEntity

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db)]


@router.get("/v1/books",summary="Retrieve all the books",status_code=200,
            tags=["books"])
async def get_all_books(db: SessionDep) -> list:
    """
    Return all the available books from the database
    :return: list
    """
    print("Retrieving all books")
    return db.query(BookEntity).all()


@router.get("/v1/books/{id}",summary="Retrieve a Book by its ID",
            status_code=200 , responses={404 : {"description": "Book ID not found"}},  tags=["books"])
async def get_book_by_id(id:int , db: SessionDep) -> BookEntity:
    """
    Return a book based on the given ID
    :return: BookEntity
    """
    print(f"Retrieving Book details for given id : {id}")
    book = (db.query(BookEntity)
            .filter(BookEntity.id == id).first())
    if not book:
        raise HTTPException(404 , "Book ID not found")
    return book


@router.post("/v1/books", summary="Create a new Book entry",
            status_code=201 ,  tags=["books"])
async def create_book(book_data:BookEntity , db: SessionDep) -> BookEntity:
    """
    Create a new Book Entry in the database
    :param db:
    :param book_data:
    :return: BookEntity
    """
    print(f"Creating a book entry for {book_data}")
    db.add(book_data)
    db.commit()
    db.refresh(book_data)
    return book_data




@router.put("/v1/books/{id}" , summary="Update a Book entry based on the given Id",
            status_code=200 , responses={404 : {"description": "Given Book Id not found"}}, tags=["books"])
async def update_book(id: int , book_entry: BookEntity , db:SessionDep) -> dict:
    """
    Update a Book entry based on the given ID
    :param db:
    :param book_entry:
    :param id:
    :return:
    """
    print(f"Updating the book entry for the given id {id}")
    book_session = db.get(BookEntity , id)
    if not book_session:
        raise HTTPException(404,"Book ID not found")
    book_data = book_entry.model_dump(exclude_unset=True)
    book_session.sqlmodel_update(book_data)
    db.commit()
    return book_data


@router.delete("/v1/books/{id}" , summary="Delete a Book entry based on the given Id",
               status_code=204 , responses={404 : {"description": "Given Book Id not found"}}, tags=["books"])
async def delete_book(id: int , db:SessionDep):
    """
    Delete a Book entry based on the given Id
    :param db:
    :param id:
    :return:
    """
    book_entry = db.get(BookEntity, id)
    if not book_entry:
        raise HTTPException(404,"Book ID not found")
    db.delete(book_entry)
    db.commit()
    return {"Book Entry Deleted": "ok"}



