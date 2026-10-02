import os
import sys
import uvicorn

# Ensure the backend directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"☁️ Starting cozy.ai server at http://{host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=True, app_dir=BACKEND_DIR)
