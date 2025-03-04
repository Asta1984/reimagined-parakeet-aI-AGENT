# app/main.py
import uvicorn
from fastapi import FastAPI
from app.routers import call_router
from app.config.settings import settings
from app.utils.logger import setup_logging

def create_app():
    # Setup logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title="Sales Voice Agent",
        description="AI-powered sales voice communication platform"
    )
    
    # Include routers
    app.include_router(call_router.router, prefix="/api/v1/calls")
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=5000, 
        reload=settings.DEBUG
    )