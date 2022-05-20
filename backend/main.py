from fastapi import FastAPI

from backend.database.session import Base, db, engine
from backend.api.v1.api import api_router


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix='/api/v1')


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()
