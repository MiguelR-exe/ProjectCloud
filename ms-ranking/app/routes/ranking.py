from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

# Puertos definidos en la infraestructura del proyecto
USERS_SERVICE_URL = "http://localhost:8001/api/users"
PARTIDAS_SERVICE_URL = "http://localhost:8003/api/sessions"

async def get_external_data(url: str):
    async with httpx.AsyncClient() as client:
        try:
            # Timeout de 5 segundos para evitar bloqueos
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en comunicación: {str(e)}")

@router.get("/leaderboard")
async def get_leaderboard():
    # Obtiene datos de ms-partidas (8003) y ms-usuarios (8001)
    sessions = await get_external_data(PARTIDAS_SERVICE_URL)
    users = await get_external_data(USERS_SERVICE_URL)
    
    # Agrupar puntajes por ID de usuario
    scores = {}
    for s in sessions:
        u_id = str(s.get("userId"))
        scores[u_id] = scores.get(u_id, 0) + s.get("score", 0)
        
    # Unir con nombres de usuario y crear lista final
    leaderboard = []
    for u in users:
        u_id = str(u.get("id"))
        if u_id in scores:
            leaderboard.append({
                "userId": u_id,
                "username": u.get("username"),
                "totalScore": scores[u_id]
            })
            
    return sorted(leaderboard, key=lambda x: x["totalScore"], reverse=True)

@router.get("/top10")
async def get_top10():
    # Reutiliza la lógica del leaderboard y extrae los 10 mejores
    full_ranking = await get_leaderboard()
    return full_ranking[:10]

@router.get("/user/{userId}")
async def get_user_ranking(userId: str):
    # Localiza la posición de un usuario específico en la lista global[cite: 1]
    leaderboard = await get_leaderboard()
    for index, entry in enumerate(leaderboard):
        if str(entry["userId"]) == str(userId):
            return {"rank": index + 1, "data": entry}
    raise HTTPException(status_code=404, detail="Usuario no participa en el ranking")

@router.get("/game/{gameId}")
async def get_ranking_by_game(gameId: str):
    # Filtra sesiones específicas por ID de juego desde ms-partidas[cite: 1]
    url_game_sessions = f"{PARTIDAS_SERVICE_URL}/game/{gameId}"
    game_sessions = await get_external_data(url_game_sessions)
    users = await get_external_data(USERS_SERVICE_URL)
    
    # Procesar solo las sesiones del juego solicitado
    game_scores = {}
    for s in game_sessions:
        u_id = str(s.get("userId"))
        game_scores[u_id] = game_scores.get(u_id, 0) + s.get("score", 0)
        
    # Cruzar con información de usuarios
    game_leaderboard = []
    for u in users:
        u_id = str(u.get("id"))
        if u_id in game_scores:
            game_leaderboard.append({
                "userId": u_id,
                "username": u.get("username"),
                "gameScore": game_scores[u_id]
            })
            
    return {
        "gameId": gameId,
        "ranking": sorted(game_leaderboard, key=lambda x: x["gameScore"], reverse=True)
    }
