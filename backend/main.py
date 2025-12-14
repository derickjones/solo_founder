#!/usr/bin/env python3
"""
Main entry point for the Gospel Study API
This file serves as the entry point for Google Cloud Run deployment
"""

import uvicorn
from search.api import app

if __name__ == "__main__":
    # Get port from environment variable or default to 8080
    import os
    port = int(os.environ.get("PORT", 8080))
    
    # Run the FastAPI application
    uvicorn.run(
        "search.api:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )