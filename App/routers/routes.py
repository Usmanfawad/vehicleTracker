import httpx

from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body


fake_db = {}

router = APIRouter(
    prefix="/v1",
    tags=["main"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/postLocation")
async def post_location():
    print("Home...")
    return {"200", "Success"}


@router.get("/getDistances")
async def get_distances():
    # DB Get all
    return {"200", "Success"}