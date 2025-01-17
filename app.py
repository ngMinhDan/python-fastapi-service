from fastapi import FastAPI
from contextlib import asynccontextmanager
from users.router import router as user_router
from endpoints.sqlite import create_db_and_tables


# Lifespan context manager to handle database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Ensure the database and tables are created
    yield  # Run the application
    # Cleanup actions if needed (e.g., closing connections, etc.)


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


