


from app.database import database


async def get_all_polls():
    query = "SELECT * FROM polls"
    return await database.fetch_all(query=query)
