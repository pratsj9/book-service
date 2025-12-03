from sqlmodel import SQLModel, Field


class BookEntity(SQLModel,table=True):
    id: int = Field(primary_key=True , index=True)
    title: str = Field()
    author: str = Field()
    year: int | None = Field(nullable=False)
    isbn: str | None = Field(index=True , nullable=False)
    available: bool = Field(default=True , nullable=False)

