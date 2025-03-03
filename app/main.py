from fastapi import FastAPI
from app.routers.twilio_router import router as twilio_router
from app.utils.logger import setup_logging
from app.utils.error_handling import add_exception_handlers

app = FastAPI(title="AI Voice Agent")
app.include_router(twilio_router, prefix="/api/v1")
add_exception_handlers(app)
setup_logging()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)