"""
Main FastAPI application file for the Agentic AI Platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes import agent_routes, user_routes, auth_routes
from core.config import settings
from db.mongodb import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
app.include_router(agent_routes.router, prefix="/api/agents", tags=["agents"])
app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])


# Events
@app.on_event("startup")
async def startup():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()


# Health check endpoint
@app.get("/api/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "version": settings.PROJECT_VERSION}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        log_level="info",
    )
