from fastapi import FastAPI

from app.database import db_shutdown, db_startup

app = FastAPI(
    title='cloudstorage'
)


@app.on_event('startup')
def startup() -> None:
    db_startup()


@app.on_event('shutdown')
async def shutdown() -> None:
    await db_shutdown()
