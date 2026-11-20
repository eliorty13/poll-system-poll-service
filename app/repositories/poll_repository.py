


from app.database import database


async def get_all_polls():
    query = "SELECT * FROM polls"
    return await database.fetch_all(query=query)



async def create_poll(question_title, first_option, second_option, third_option, fourth_option):
    query = """
        INSERT INTO polls (
            question_title,
            first_option,
            second_option,
            third_option,
            fourth_option
        )
        VALUES (
            :question_title,
            :first_option,
            :second_option,
            :third_option,
            :fourth_option
        )
    """

    values = {
        "question_title": question_title,
        "first_option": first_option,
        "second_option": second_option,
        "third_option": third_option,
        "fourth_option": fourth_option
    }

    return await database.execute(query=query, values=values)



async def get_poll_by_id(poll_id: int):
    query = """
        SELECT * FROM polls
        WHERE poll_id = :poll_id
    """

    values = {"poll_id": poll_id}

    return await database.fetch_one(
        query=query,
        values=values
    )




async def update_poll(poll_id: int, poll_data):
    query = """
        UPDATE polls
        SET question_title = :question_title,
            first_option = :first_option,
            second_option = :second_option,
            third_option = :third_option,
            fourth_option = :fourth_option
        WHERE poll_id = :poll_id
    """

    values = {
        "poll_id": poll_id,
        "question_title": poll_data.question_title,
        "first_option": poll_data.first_option,
        "second_option": poll_data.second_option,
        "third_option": poll_data.third_option,
        "fourth_option": poll_data.fourth_option
    }

    await database.execute(query=query, values=values)




async def delete_poll(poll_id: int):
    query = """
        DELETE FROM polls
        WHERE poll_id = :poll_id
    """

    values = {"poll_id": poll_id}

    await database.execute(
        query=query,
        values=values
    )


async def create_vote(user_id: int, poll_id: int, selected_option: int):
    query = """
        INSERT INTO votes (
            user_id,
            poll_id,
            selected_option
        )
        VALUES (
        :user_id,
        :poll_id,
        :selected_option
        )
    """
    values = {
        "user_id": user_id,
        "poll_id": poll_id,
        "selected_option": selected_option
    }

    return await database.execute(
        query=query,
        values=values
    )



async def get_vote_by_user_and_poll(user_id: int, poll_id: int):
    query = """
    SELECT * FROM votes
    WHERE user_id = :user_id
    AND poll_id = :poll_id
    """


    values = {
        "user_id": user_id,
        "poll_id": poll_id
    }

    return await database.fetch_one(
        query=query,
        values=values
    )

async def update_vote(user_id: int, poll_id: int, selected_option: int):
    query = """
    UPDATE votes
    SET selected_option = :selected_option
    WHERE user_id = :user_id
    AND poll_id = :poll_id
    """


    values = {
        "user_id": user_id,
        "poll_id": poll_id,
        "selected_option": selected_option
    }

    await database.execute(
        query=query,
        values=values
    )

    return await get_vote_by_user_and_poll(user_id, poll_id)


async def delete_vote(user_id: int, poll_id: int):
    query = """
    DELETE FROM votes
    WHERE user_id = :user_id
    AND poll_id = :poll_id
    """

    values = {
        "user_id": user_id,
        "poll_id": poll_id
    }


    await database.execute(
        query=query,
        values=values
    )


async def get_votes_by_poll_id(poll_id: int):
    query = """
    SELECT * FROM votes
    WHERE poll_id = :poll_id
    """

    return await database.fetch_all(
        query=query,
        values={"poll_id": poll_id}
)

async def count_votes_by_poll_id(poll_id: int):
    query = """
    SELECT COUNT(*) FROM votes
    WHERE poll_id = :poll_id
    """


    return await database.fetch_val(
        query=query,
        values={"poll_id": poll_id}
    )

async def count_votes_by_option(poll_id: int):
    query = """
    SELECT selected_option, COUNT(*) AS vote_count
    FROM votes
    WHERE poll_id = :poll_id
    GROUP BY selected_option
    ORDER BY selected_option
    """

    results = await database.fetch_all(
        query=query,
        values={"poll_id": poll_id}
    )

    return [dict(row) for row in results]


async def get_votes_by_user_id(user_id: int):
    query = """
    SELECT vote_id, poll_id, selected_option
    FROM votes
    WHERE user_id = :user_id
    ORDER BY poll_id
    """

    results = await database.fetch_all(
        query=query,
        values={"user_id": user_id}
    )

    return [dict(row) for row in results]


async def delete_votes_by_user_id(user_id: int):
    query = """
    DELETE FROM votes
    WHERE user_id = :user_id
    """

    await database.execute(
        query=query,
        values={"user_id": user_id}
    )