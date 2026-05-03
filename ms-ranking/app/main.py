from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ranking

app = FastAPI(title="MS-Ranking Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ranking.router, prefix="/api/ranking", tags=["Ranking"])

@app.get("/")
async def root():
    return {
        "service": "ms-ranking",
        "status": "online",
        "endpoints": [
            "/api/ranking/leaderboard",
            "/api/ranking/user/{userId}",
            "/api/ranking/top10",
            "/api/ranking/game/{gameId}"
        ]
    }
