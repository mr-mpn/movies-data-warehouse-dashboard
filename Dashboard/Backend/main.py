import sys
sys.path.append(".")
from fastapi import FastAPI, HTTPException
from Dashboard.Backend.DTO.models import UserSignUp
from Module.mongo_connector import users_collection

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "alive"}

@app.post("/sign_up")
async def sign_up_user(user: UserSignUp):
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    await users_collection.insert_one({
        "username": user.username,
        "password": user.password
    })
    return {"message": "User created successfully"}

