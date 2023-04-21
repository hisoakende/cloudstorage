from fastapi import FastAPI

from app.database import db_shutdown, db_startup
from app.routers.files import router

app = FastAPI(
    title='cloudstorage'
)

app.include_router(
    router
)


@app.on_event('startup')
def startup() -> None:
    db_startup()


@app.on_event('shutdown')
async def shutdown() -> None:
    await db_shutdown()
