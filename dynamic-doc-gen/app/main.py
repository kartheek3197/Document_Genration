"""
Entry point of the FastAPI application. Defines the application instance and includes API routers.
"""
from fastapi import FastAPI
from app.api import routes

# Create FastAPI application
app = FastAPI(
    title="Dynamic Document Generation API",
    description="An API for generating documents with dynamic content using multiple AI agents.",
    version="0.1.0"
)

# Include API routes from the routes module.
app.include_router(routes.router)

@app.get("/")
async def read_root():
    """
    Root endpoint for health check or basic info.
    """
    return {"status": "ok", "message": "Dynamic Document Generation API is running."}

# When running directly (not via uvicorn CLI), start the server.
if __name__ == "__main__":
    import uvicorn
    # Run the app with Uvicorn server.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
