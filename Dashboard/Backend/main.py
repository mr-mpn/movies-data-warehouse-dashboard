import sys
sys.path.append(".")
from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from Dashboard.Backend.DTO.models import UserSignUp
from Module.mongo_connector import users_collection

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"])

@app.get("/health")
def health():
    return {"message": "Backend is working and alive"}

@app.post("/sign_up")
async def sign_up_user(user: UserSignUp):
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    await users_collection.insert_one({
        "username": user.username,
        "password": pwd_context.hash(user.password)
    })
    return {"message": "User created successfully"}

@app.post("/log_in")
async def validate_log_in(user: UserSignUp):
    try:
        existing = await users_collection.find_one({"username": user.username})
        if not existing:
            raise HTTPException(status_code=404, detail="User not found")
        
        password_validated = pwd_context.verify(user.password, existing["password"])
        if not password_validated:
            raise HTTPException(status_code=401, detail="Password is not correct")
        
        return {"message": "Password was correct"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")