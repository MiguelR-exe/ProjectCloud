from fastapi import FastAPI
from app.routes import analytics

app = FastAPI(title="MS-Analytics Service")

app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/")
async def root():
    return {
        "service": "ms-analytics",
        "status": "online"
    }

@app.get("/analytics/health")
def health_analytics_prefixed():
    return {
        "status": "ok",
        "service": "ms-analytics"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ms-analytics"
    }
