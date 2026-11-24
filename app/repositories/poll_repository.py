


from app.database import database


async def get_all_polls():
    query = "SELECT * FROM polls"
    return await database.fetch_all(query=query)



async def create_poll(question_title, options):
    async with database.transaction():

        poll_query = """
            INSERT INTO polls (question_title)
            VALUES (:question_title)
        """

        poll_id = await database.execute(
            query=poll_query,
            values={"question_title": question_title}
        )

        option_query = """
            INSERT INTO poll_options (poll_id, option_text)
            VALUES (:poll_id, :option_text)
        """

        for option in options:
            await database.execute(
                query=option_query,
                values={
                    "poll_id": poll_id,
                    "option_text": option
                }
            )

        return poll_id



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


async def get_options_by_poll_id(poll_id: int):
    query = """
        SELECT option_id, option_text
        FROM poll_options
        WHERE poll_id = :poll_id
        ORDER BY option_id
    """

    return await database.fetch_all(
        query=query,
        values={"poll_id": poll_id}
    )


async def get_option_by_id(poll_id: int, option_id: int):
    query = """
        SELECT option_id, option_text
        FROM poll_options
        WHERE poll_id = :poll_id
        AND option_id = :option_id
    """

    return await database.fetch_one(
        query=query,
        values={
            "poll_id": poll_id,
            "option_id": option_id
        }
    )



async def update_poll(poll_id: int, poll_data):
    async with database.transaction():

        question_query = """
            UPDATE polls
            SET question_title = :question_title
            WHERE poll_id = :poll_id
        """

        await database.execute(
            query=question_query,
            values={
                "poll_id": poll_id,
                "question_title": poll_data.question_title
            }
        )

        delete_query = """
            DELETE FROM poll_options
            WHERE poll_id = :poll_id
        """

        await database.execute(
            query=delete_query,
            values={"poll_id": poll_id}
        )

        insert_query = """
            INSERT INTO poll_options (poll_id, option_text)
            VALUES (:poll_id, :option_text)
        """

        for option in poll_data.options:
            await database.execute(
                query=insert_query,
                values={
                    "poll_id": poll_id,
                    "option_text": option
                }
            )

async def delete_poll(poll_id: int):

    values = {"poll_id": poll_id}

    async with database.transaction():

        await database.execute(
            query="DELETE FROM votes WHERE poll_id = :poll_id",
            values=values
        )

        await database.execute(
            query="DELETE FROM poll_options WHERE poll_id = :poll_id",
            values=values
        )

        await database.execute(
            query="DELETE FROM polls WHERE poll_id = :poll_id",
            values=values
        )


async def create_vote(user_id: int, poll_id: int, option_id: int):
    query = """
        INSERT INTO votes (
            user_id,
            poll_id,
            option_id
        )
        VALUES (
            :user_id,
            :poll_id,
            :option_id
        )
    """

    values = {
        "user_id": user_id,
        "poll_id": poll_id,
        "option_id": option_id
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


async def update_vote(user_id: int, poll_id: int, option_id: int):
    query = """
        UPDATE votes
        SET option_id = :option_id
        WHERE user_id = :user_id
        AND poll_id = :poll_id
    """

    values = {
        "user_id": user_id,
        "poll_id": poll_id,
        "option_id": option_id
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
        SELECT option_id, COUNT(*) AS vote_count
        FROM votes
        WHERE poll_id = :poll_id
        GROUP BY option_id
    """

    return await database.fetch_all(
        query=query,
        values={"poll_id": poll_id}
    )


async def get_votes_by_user_id(user_id: int):
    query = """
    SELECT vote_id, poll_id, option_id
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