
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Depends
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import auth, notes, tags, contacts, users

from src.conf.config import config

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(notes.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@app.on_event("startup")
async def startup():
    """
    Startup event handler.
    Initialize Redis connection and FastAPILimiter.
    """
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD)
    await FastAPILimiter.init(r)


@app.get("/")
def index():
    """
    Home endpoint.
    Returns a welcome message.
    """
    return {"message": "Contacts Application"}


@app.get("/api/healthecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Health checker endpoint.
    Checks database connection status.

    :param db: AsyncSession instance for database interaction.
    :return: Health status message.
    """
    try:
        # Make request
        result = await db.execute(text("SELECT 1;"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error connecting to the database")