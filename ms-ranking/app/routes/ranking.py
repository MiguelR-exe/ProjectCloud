from fastapi import APIRouter, HTTPException
import httpx
import os
import time

router = APIRouter()

MS_USUARIOS_BASE     = os.getenv("MS_USUARIOS_URL", "http://ms-usuarios:8001")
SCORES_URL = os.getenv("MS_PARTIDAS_URL", "http://ms-partidas:8080") + "/api/sessions/stats/scores"

_cache = {"leaderboard": None, "ts": 0}
CACHE_TTL = 300  # 5 minutos

async def get_external_data(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=60.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en comunicación: {str(e)}")

async def build_leaderboard():
    if _cache["leaderboard"] and (time.time() - _cache["ts"]) < CACHE_TTL:
        return _cache["leaderboard"]

    # Scores agregados por la DB — mucho más rápido que bajar todas las sesiones
    score_rows = await get_external_data(SCORES_URL)
    scores = {str(r["userId"]): r["totalScore"] for r in score_rows}

    limit = len(scores)
    users = await get_external_data(f"{MS_USUARIOS_BASE}/api/users/?skip=0&limit={limit}")
    user_map = {str(u.get("id")): u.get("username") for u in users}

    result = sorted([
        {"userId": u_id, "username": user_map.get(u_id, u_id), "totalScore": total}
        for u_id, total in scores.items() if u_id in user_map
    ], key=lambda x: x["totalScore"], reverse=True)

    _cache["leaderboard"] = result
    _cache["ts"] = time.time()
    return result

@router.get("/leaderboard")
async def get_leaderboard():
    return await build_leaderboard()

@router.get("/user/{userId}")
async def get_user_ranking(userId: str):
    leaderboard = await get_leaderboard()
    for index, entry in enumerate(leaderboard):
        if str(entry["userId"]) == str(userId):
            return {"rank": index + 1, "data": entry}
    raise HTTPException(status_code=404, detail="Usuario no participa en el ranking")
