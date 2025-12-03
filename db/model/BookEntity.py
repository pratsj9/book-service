from sqlmodel import SQLModel, Field


class BookEntity(SQLModel,table=True):
    id: int = Field(primary_key=True , index=True)
    title: str = Field(description="The title of the Book")
    author: str = Field(description="The author of the Book")
    year: int | None = Field(nullable=False , description="Launch Year of this edition")
    isbn: str | None = Field(index=True , nullable=False, description="ISBN number")
    available: bool = Field(default=True , nullable=False , description="Is the book currently available")

