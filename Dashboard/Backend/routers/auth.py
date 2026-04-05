import sys
sys.path.append(".")
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from Dashboard.Backend.DTO.models import AuthenticationRequest,AuthenticationResponse
from Module.mongo_connector import users_collection

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"])



@router.post("/sign_up")
async def sign_up_user(user: AuthenticationRequest)->AuthenticationResponse:
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    await users_collection.insert_one({
        "username": user.username,
        "password": pwd_context.hash(user.password)
    })
    return {"message": "User created successfully"}



@router.post("/log_in")
async def validate_log_in(user: AuthenticationRequest)->AuthenticationResponse:
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