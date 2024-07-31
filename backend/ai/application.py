import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from myproyect.openai import ai_route


app = FastAPI()

app.include_router(ai_route)


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
