from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from myproject.users import users_route
from myproject.topics import topics_route
from myproject.threads import threads_route
from myproject.oauth import oauth_route
from myproject.mixed import mixed_route

app = FastAPI()

app.include_router(users_route)
app.include_router(topics_route)
app.include_router(threads_route)
app.include_router(oauth_route)
app.include_router(mixed_route)

# Add CORS to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
