#!/usr/bin/env python3
"""
Main application entry point for Movember AI Rules System
"""

# Import the FastAPI app from our API module
from api.movember_api import app

# This allows Render to find the app at the root level
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 