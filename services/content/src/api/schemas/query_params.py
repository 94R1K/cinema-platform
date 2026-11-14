from typing import Self

from pydantic import BaseModel, Field, model_validator


MAX_RESULT_WINDOW = 10_000

class PaginationParams(BaseModel):
    page_size: int = Field(default=50, ge=1, le=100)
    page_number: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def validate_pagination(self) -> Self:
        if self.page_number * self.page_size > MAX_RESULT_WINDOW:
            raise ValueError(
                f"The requested page exceeds the maximum result window of "
                f"{MAX_RESULT_WINDOW}"
            )
        return self
