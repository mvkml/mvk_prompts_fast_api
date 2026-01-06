'''
Docstring for main
VISHNU KIRAN M 
Description: sample fast api which will help you to start work on AI process
'''

from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI(title="MARVISH Industrial AI Assistant", version="1.0.0",
              description="Description."
              )

@app.get("/")
def api_init():
    return {"message": "API initialized"}

# Optional: allow `python -m app.main`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.25", port=825, reload=True)


