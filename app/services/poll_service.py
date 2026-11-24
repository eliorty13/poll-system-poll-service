



from app.repositories import poll_repository
from fastapi import HTTPException
import httpx
from app.config import Config



async def get_all_polls():
    polls = await poll_repository.get_all_polls()

    all_polls = []

    for poll in polls:
        poll_id = poll["poll_id"]

        options = await poll_repository.get_options_by_poll_id(poll_id)

        all_polls.append({
            "poll_id": poll_id,
            "question_title": poll["question_title"],
            "options": [dict(option) for option in options]
        })

    return all_polls



async def create_poll(poll_data):
    normalized_options = []

    for option in poll_data.options:
        normalized_options.append(option.lower())

    if len(normalized_options) != len(set(normalized_options)):
        raise ValueError("Poll options must be unique")

    poll_id = await poll_repository.create_poll(
        question_title=poll_data.question_title,
        options=poll_data.options
    )

    return {
        "poll_id": poll_id,
        "message": "Poll created successfully"
    }

async def get_poll_by_id(poll_id: int):
    poll = await poll_repository.get_poll_by_id(poll_id)

    if poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    options = await poll_repository.get_options_by_poll_id(poll_id)


    return {
        "poll_id": poll["poll_id"],
        "question_title": poll["question_title"],
        "options": [dict(option) for option in options]
    }



async def update_poll(poll_id: int, poll_data):
    existing_poll = await poll_repository.get_poll_by_id(poll_id)

    if existing_poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    existing_votes = await poll_repository.get_votes_by_poll_id(poll_id)

    if existing_votes:
        raise HTTPException(
            status_code=409,
            detail="Cannot update a poll that already has votes"
        )
    normalized_options = []

    for option in poll_data.options:
        normalized_options.append(option.lower())

    if len(normalized_options) != len(set(normalized_options)):
        raise ValueError("Poll options must be unique")

    await poll_repository.update_poll(poll_id, poll_data)

    return {
        "poll_id": poll_id,
        "message": "Poll updated successfully"
    }



async def delete_poll(poll_id: int):
    existing_poll = await poll_repository.get_poll_by_id(poll_id)

    if existing_poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    await poll_repository.delete_poll(poll_id)

    return {
        "poll_id": poll_id,
        "message": "Poll deleted successfully"
    }


async def check_user_registration(user_id: int):
    url = f"{Config().USER_SERVICE_URL}/users/{user_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 404:
            return False


        response.raise_for_status()

        user_data = response.json()

        return user_data.get("is_registered") == 1


async def create_vote(user_id: int, poll_id: int, option_id: int):

    existing_poll = await poll_repository.get_poll_by_id(poll_id)

    if existing_poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )


    option = await poll_repository.get_option_by_id(
        poll_id=poll_id,
        option_id=option_id
    )

    if option is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid option for this poll"
        )


    is_registered = await check_user_registration(user_id)

    if not is_registered:
        raise HTTPException(
            status_code=403,
            detail="User not registered"
        )


    existing_vote = await poll_repository.get_vote_by_user_and_poll(
        user_id=user_id,
        poll_id=poll_id
    )

    if existing_vote is not None:
        raise HTTPException(
            status_code=409,
            detail="User has already voted in this poll"
        )


    vote_id = await poll_repository.create_vote(
        user_id=user_id,
        poll_id=poll_id,
        option_id=option_id
    )

    return {
        "vote_id": vote_id,
        "user_id": user_id,
        "poll_id": poll_id,
        "option_id": option_id

    }



async def update_vote(user_id: int, poll_id: int, option_id: int):
    existing_poll = await poll_repository.get_poll_by_id(poll_id)

    if existing_poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    option = await poll_repository.get_option_by_id(
        poll_id=poll_id,
        option_id=option_id
    )

    if option is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid option for this poll"
        )

    is_registered = await check_user_registration(user_id)

    if not is_registered:
        raise HTTPException(
            status_code=403,
            detail="User is not registered"
        )

    existing_vote = await poll_repository.get_vote_by_user_and_poll(
        user_id=user_id,
        poll_id=poll_id
    )

    if existing_vote is None:
        raise HTTPException(
            status_code=404,
            detail= "Vote not found"
        )

    updated_vote = await poll_repository.update_vote(
        user_id=user_id,
        poll_id=poll_id,
        option_id=option_id
    )

    return dict(updated_vote)


async def delete_vote(user_id: int, poll_id: int):

    existing_vote = await poll_repository.get_vote_by_user_and_poll(
        user_id=user_id,
        poll_id=poll_id
    )

    if existing_vote is None:
        raise HTTPException(
            status_code=404,
            detail= "Vote not found"
        )

    await poll_repository.delete_vote(
        user_id=user_id,
        poll_id=poll_id
    )

    return {"message": "Vote deleted successfully"}


async def get_poll_vote_count(poll_id: int):

    poll = await poll_repository.get_poll_by_id(poll_id)

    if poll is None:
        raise HTTPException(
            status_code=404,
            detail= "Poll not found"
        )


    total_votes = await poll_repository.count_votes_by_poll_id(poll_id)

    return {
        "poll_id": poll_id,
        "total_votes": total_votes,
    }

async def get_poll_option_results(poll_id: int):
    poll = await poll_repository.get_poll_by_id(poll_id)

    if poll is None:
        raise HTTPException(
            status_code=404,
            detail= "Poll not found"
        )

    results = await poll_repository.count_votes_by_option(poll_id)

    options = await poll_repository.get_options_by_poll_id(poll_id)

    vote_counts = {
        option["option_id"]: 0
        for option in options
    }

    for result in results:
        option = result["option_id"]

        vote_counts[option] = result["vote_count"]

    total_votes = sum(vote_counts.values())

    return {
        "poll_id": poll_id,
        "total_votes": total_votes,
        "results": [
            {
                "option_id": option["option_id"],
                "option_text": option["option_text"],
                "vote_count": vote_counts[option["option_id"]]
            }
            for option in options
        ]
    }


async def get_user_vote_history(user_id: int):

    votes = await poll_repository.get_votes_by_user_id(user_id)

    total_answered = len(votes)

    return {
        "user_id": user_id,
        "total_questions_answered": total_answered,
        "answers": votes,
    }



async def get_all_poll_results():
    polls = await get_all_polls()

    all_results = []

    for poll in polls:
        poll_id = poll["poll_id"]

        results = await get_poll_option_results(poll_id)

        all_results.append(results)

    return {
        "total_polls": len(all_results),
        "poll_results": all_results
    }



async def delete_all_user_votes(user_id: int):

    await poll_repository.delete_votes_by_user_id(user_id)

    return {
        "message": "user votes deleted successfully",
        "user_id": user_id
    }
