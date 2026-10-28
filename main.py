
from fastapi import FastAPI

from routers.auth import router as auth_router
from routers.users import router as users_router

app = FastAPI(title="Library API")

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def home():
    return {"message": "Library API is running!"}
