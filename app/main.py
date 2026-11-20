


from fastapi import FastAPI
from app.database import database
from app.controllers.poll_controller import router as poll_router



app = FastAPI()

app.include_router(poll_router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def home():
    return {"message": "Poll Service is running"}
