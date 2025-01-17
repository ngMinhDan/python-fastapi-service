from fastapi import APIRouter, HTTPException
from users.schema import UserRegistration
from utils.security import hash_password
from users.model import User
from endpoints.sqlite import SessionDep
from aiohttp import ClientSession
import asyncio

router = APIRouter(prefix="/api/v1")

# normal api with working with sqlite 
# but bellow code dont wirte by asyncio code, because sqlmodel doest support full asyncio code
@router.post("/register")
def register_user(user_input: UserRegistration, session: SessionDep):
    user = User.find_by_email(session, user_input.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")
    else:
        hashed_password = hash_password(user_input.password)
        new_user = User(email=user_input.email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"data": "Register done !"}

# api with designed for powerful of asyncIO code with IO not blocking
@router.get("/aggregate/")
async def aggregate_data():
    async with ClientSession() as session:
        # Define the URLs to fetch
        urls = [
            "https://jsonplaceholder.typicode.com/posts",
            "https://jsonplaceholder.typicode.com/comments",
            "https://jsonplaceholder.typicode.com/todos",
        ]

        # Create tasks for concurrent fetching
        tasks = [session.get(url) for url in urls]

        # Fetch all data concurrently
        responses = await asyncio.gather(*tasks)

        # Process responses (extract JSON)
        results = [await response.json() for response in responses]

        return {
            "posts": results[0][0],  # Data from the first URL
            "comments": results[1][0],  # Data from the second URL
            "todos": results[2][0],  # Data from the third URL
        }