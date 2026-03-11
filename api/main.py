from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import users_collection
from passlib.context import CryptContext
from pydantic import BaseModel, field_validator,EmailStr
import sys
import os

sys.path.append(os.path.abspath(".."))
from model.recommender import recommend_by_ingredients

app = FastAPI()
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)
class UserLogin(BaseModel):
    email:EmailStr
    password:str
class UserSignup(BaseModel):
    email:EmailStr
    password:str
    @field_validator("password")
    def password_strength(cls,value):
        if len(value)<6:
            raise ValueError("Password must be atleast 6 characters")
        return value
def hash_password(password:str):
    return pwd_context.hash(password)

# ---------------------------
# CORS Configuration
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecipeRequest(BaseModel):
    ingredients: str
    match_mode: str = "any"
    max_calories: int | None = None
    high_protein: bool = False

    @field_validator("ingredients")
    def ingredient_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Ingredient cannot be empty")
        return value

@app.get("/")
def home():
    return {"message": "Recipe API is running"}

@app.post("/recommend")
def recommend(request: RecipeRequest):

    results = recommend_by_ingredients(
        user_input=request.ingredients,
        match_mode=request.match_mode,
        max_calories=request.max_calories,
        high_protein=request.high_protein
    )

    if not results:
        return {
            "message": "No recipe found",
            "results": []
        }

    return {
        "message": "Success",
        "results": results
    }
@app.post("/signup")
def signup(user: UserSignup):
    existing_user=users_collection.find_one({"email":user.email})
    if existing_user:
        raise HTTPException(status_code=400,detail="User Already registered")
    hashed_password=hash_password(user.password)
    users_collection.insert_one({
        "email":user.email,
        "password":hashed_password
    })
    return {"message":"Account Created Successfully"}
@app.post("/login")
def login(user:UserLogin):
    db_user=users_collection.find_one({"email":user.email})
    if not db_user:
        raise HTTPException(status_code=404,detail="User not registered")
    if not verify_password(user.password,db_user["password"]):
        raise HTTPException(status_code=401,detail="Invalid Password")
    return{
        "message":"Login Successful",
        "email":str(db_user["email"])
    }