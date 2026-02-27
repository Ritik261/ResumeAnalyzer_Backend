from fastapi import FastAPI
from dotenv import load_dotenv
from app.database.database import Base,engine
from app.routing.endpoints import router
from app.routing.resume import router1
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

Base.metadata.create_all(bind = engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5000",
        "http://localhost:5000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"message":"fastapi working"}

app.include_router(router)
app.include_router(router1)
