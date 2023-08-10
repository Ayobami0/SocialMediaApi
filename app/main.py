from fastapi import FastAPI

from auth.authenticate import auth_route
from routes.user import user_route
from routes.general import general_route
from database.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_route)
app.include_router(general_route)
app.include_router(auth_route)
