from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from auth.authenticate import auth_route
from routes.user import user_route
from routes.general import general_route
from database.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_route)
app.include_router(general_route)
app.include_router(auth_route)


@app.get('/', tags=['Documentation'])
async def api_doc():
    return RedirectResponse("/docs#/general/get_all_posts_all_posts_get")
