from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..domain.models import Book


class BookIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1)
    pages: int | None = Field(default=None, gt=0)
    genre: str = Field(default="", alias="category")

    @field_validator("pages", mode="before")
    @classmethod
    def unknown_pages(cls, value: object) -> object:
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return None  # «за домовленістю» / «невідомо»
        return value

    @field_validator("title", "author")
    @classmethod
    def strip_spaces(cls, value: str) -> str:
        return " ".join(value.split())

    @field_validator("title")
    @classmethod
    def lowercase(cls, value: str) -> str:
        return value.lower()

    def to_domain(self) -> Book:
        return Book(
            title=self.title,
            author=self.author,
            pages=self.pages,
            genre=self.genre,
        )
