import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app_result",
        host="127.0.0.1",
        port=8002,
        reload=False  # Optional: enables auto-reload on file changes
    )