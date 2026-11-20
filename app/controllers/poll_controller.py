



from fastapi import APIRouter
from app.services import poll_service
from app.schemas.poll_schema import PollCreate
from app.schemas.vote_schema import VoteCreate
from app.services import poll_service

router = APIRouter()


@router.get("/polls")
async def get_all_polls():
    return await poll_service.get_all_polls()


@router.post("/polls", status_code=201)
async def create_poll(poll_data: PollCreate):
    return await poll_service.create_poll(poll_data)


@router.get("/polls/{poll_id}")
async def get_poll_by_id(poll_id: int):
    return await poll_service.get_poll_by_id(poll_id)


@router.put("/polls/{poll_id}")
async def update_poll(poll_id: int, poll_data: PollCreate):
    return await poll_service.update_poll(poll_id, poll_data)


@router.delete("/polls/{poll_id}")
async def delete_poll(poll_id: int):
    return await poll_service.delete_poll(poll_id)

@router.post("/votes", status_code=201)
async def submit_vote(vote: VoteCreate):
    return await poll_service.create_vote(
        user_id=vote.user_id,
        poll_id=vote.poll_id,
        selected_option=vote.selected_option
    )

@router.put("/votes/{user_id}/{poll_id}")
async def update_vote(user_id: int, poll_id: int, selected_option: int):
    return await poll_service.update_vote(
        user_id=user_id,
        poll_id=poll_id,
        selected_option=selected_option
    )

@router.delete("/votes/{user_id}/{poll_id}")
async def delete_vote(user_id: int, poll_id: int):
    return await poll_service.delete_vote(
        user_id=user_id,
        poll_id=poll_id
    )


@router.get("/polls/{poll_id}/vote=count")
async def get_poll_vote_count(poll_id: int):
    return await poll_service.get_poll_vote_count(poll_id)

@router.get("/polls/{poll_id}/results")
async def get_poll_option_results(poll_id: int):
    return await poll_service.get_poll_option_results(poll_id)


@router.get("/users/{user_id}/votes")
async def get_user_vote_history(user_id: int):
    return await poll_service.get_user_vote_history(user_id)


@router.get("/polls/results/all")
async def get_all_poll_results():
    return await poll_service.get_all_polls()

@router.delete("/users/{user_id}/votes")
async def delete_all_user_votes(user_id: int):
    return await poll_service.delete_all_user_votes(user_id)
