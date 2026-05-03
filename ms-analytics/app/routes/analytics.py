from fastapi import APIRouter, HTTPException
import boto3
import time

router = APIRouter()

ATHENA_DB = "game_analytics"
S3_OUTPUT = "s3://game-analytics-data-5/athena-results/"

athena = boto3.client('athena', region_name='us-east-1') # Ajusta la región según tu cuenta

def run_athena_query(query: str):
    try:
        # Iniciar la ejecución de la consulta
        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': ATHENA_DB},
            ResultConfiguration={'OutputLocation': S3_OUTPUT}
        )
        query_execution_id = response['QueryExecutionId']
        
        # Esperar a que la consulta termine (polling simple)
        while True:
            status = athena.get_query_execution(QueryExecutionId=query_execution_id)
            state = status['QueryExecution']['Status']['State']
            if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(1)
            
        if state != 'SUCCEEDED':
            raise Exception(f"Athena query failed: {state}")

        # Obtener resultados
        return athena.get_query_results(QueryExecutionId=query_execution_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usuarios-por-pais")
async def get_users_by_country():
    # Consulta la vista definida en el Glue Catalog
    query = "SELECT * FROM v_usuarios_por_pais"
    return run_athena_query(query)

@router.get("/top-juegos")
async def get_top_games():
    # Consulta SQL que une tablas según el PDF
    query = """
        SELECT g.name, COUNT(s.id) as total_sessions 
        FROM game_sessions s 
        JOIN games g ON s.gameId = g.id 
        GROUP BY g.name 
        ORDER BY total_sessions DESC LIMIT 5
    """
    return run_athena_query(query)

@router.get("/summary")
async def get_summary():
    # Resumen general de la plataforma
    query = "SELECT COUNT(*) as total_partidas FROM game_sessions"
    return run_athena_query(query)
