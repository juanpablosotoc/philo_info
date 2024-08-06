import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from myproyect.data import data_route
from myproyect.users import users_route


app = FastAPI()

app.include_router(data_route)
app.include_router(users_route)


# Add CORS to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setup health route for health check
@app.get("/health")
def health():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
