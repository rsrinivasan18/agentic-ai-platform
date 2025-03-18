"""
Main application entry point for the Agentic AI Platform.
"""
import uvicorn
from fastapi import FastAPI
from src.config.settings import API_HOST, API_PORT
from src.api.routes import router

app = FastAPI(
    title="Agentic AI Platform",
    description="An extensible platform for building and deploying AI agents",
    version="0.1.0"
)

# Include API routes
app.include_router(router, prefix="/api")

# Add a simple health check endpoint
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Agentic AI Platform is running"}

if __name__ == "__main__":
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)
