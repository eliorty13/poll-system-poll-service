


from pydantic import BaseModel, Field


class VoteCreate(BaseModel):
    user_id: int
    poll_id: int
    option_id: int = Field(gt=0)