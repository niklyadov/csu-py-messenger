from fastapi import FastAPI

from endpoints.user import router as user_router

app = FastAPI()

app.include_router(user_router, tags=["user"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
