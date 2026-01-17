'''
Docstring for main
VISHNU KIRAN M 
Description: sample fast api which will help you to start work on AI process
'''

from fastapi import FastAPI
from app.api.router import api_router

# Create FastAPI instance
app = FastAPI(title="VISHNU KIRAN M Industrial AI Assistant", version="1.0.0",
              description="Description."
              )

@app.get("/")
def api_init():
    return {"message": "API initialized"}

app.include_router(api_router, prefix="/api")

# # Optional: allow `python -m app.main`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.25", port=825, reload=True)
# cd C:\v\v\learn\lv_python\ai\VishAgent
# python -m uvicorn app.main:app --host 127.0.0.25 --port 825


