from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body



router = APIRouter(
    prefix="/main",
    tags=["main"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/home")
async def home():
    print("Home...")
    return {"200", "Success"}


@router.get("/")
async def index():
    print("Index...")
    return {"200", "Success"}