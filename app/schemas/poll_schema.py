

from typing import Annotated
from pydantic import StringConstraints
from pydantic import BaseModel, Field



class PollCreate(BaseModel):
    question_title: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
    options: list[
        Annotated[
            str,
            StringConstraints(strip_whitespace=True, min_length=1)
    ]
] = Field(min_length=2)