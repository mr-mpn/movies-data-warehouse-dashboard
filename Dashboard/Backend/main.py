from Dashboard.Backend.routers import auth,home,movie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"message": "Backend is working and alive"}

app.include_router(auth.router, prefix="/auth")
app.include_router(home.router)
app.include_router(movie.router)

