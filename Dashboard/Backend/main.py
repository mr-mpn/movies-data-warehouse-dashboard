from Dashboard.Backend.routers import auth,home
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"message": "Backend is working and alive"}

app.include_router(auth.router, prefix="/auth")
app.include_router(home.router)
