

from pydantic import BaseModel


class PollCreate(BaseModel):
    question_title: str
    first_option: str
    second_option: str
    third_option: str
    fourth_option: str
