


from pydantic import BaseModel, Field


class VoteCreate(BaseModel):
    user_id: int
    poll_id: int
    selected_option: int