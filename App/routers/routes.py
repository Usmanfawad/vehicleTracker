import httpx


from App.schemas.schema import Location
from App.services.utils.lat_long_parser import extract_coordinates
from App.routers.constants import *
from App.db.session import get_db

from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body, Form
from typing import Optional



router = APIRouter(
    prefix="/v1",
    tags=["main"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def main():
    '''
    Test route
    :return: Coordinates list
    '''
    coordinates_list = [extract_coordinates(url) for url in BUS_STOPS]
    return {"200": "Success", "data": coordinates_list}


@router.get("/getDistance/all", status_code=status.HTTP_200_OK)
async def get_distance_all():
    '''
    Returns distances of all busses from all the stops
    :return: Distance matrix API response
    '''
    api_responses = []
    base_url = "https://api.distancematrix.ai/maps/api/distancematrix/json"
    # DB Get all
    stops = BUS_LOCATIONS_PARSED["locationStops"]
    # Iterate
    for bus_id, bus_coordinates in FAKE_DB.items():
        print(bus_coordinates)
        for each_stop in stops:
            for stop, coordinates in each_stop.items():
                params = {
                    "origins": ",".join(map(str, bus_coordinates)),
                    "destinations": ",".join(map(str, coordinates)),
                    "key": API_KEY
                }
                async with httpx.AsyncClient() as client:
                    response = await client.get(base_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    api_responses.append(data)
                else:
                    raise HTTPException(status_code=response.status_code, detail="No response from Distance Matrix Server")

    return {"data" : api_responses}


@router.post("/postLocation")
async def post_location(
        lat: float,
        longitude: float,
        time: str,
        id: str
    ):
    '''
    GPS Logger Listener
    :param locationObj:
    :return: BOOL
    '''
    print({"lat": lat, "lon": longitude, "time": time, "id": id})
    FAKE_DB[id] = [lat,longitude]
    return {"200", "Success"}