import httpx
from typing import Optional

from sqlalchemy.orm import Session



from App.schemas.schema import Location
from App.services.utils.lat_long_parser import extract_coordinates
from App.routers.constants import *
from App.db.session import get_db
from App.services.controllers.bus import add_or_update_bus, get_all_buses


from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body, Form
from fastapi import Depends




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
async def get_distance_all(db: Session = Depends(get_db)):
    '''
    Returns distances of all busses from all the stops
    :return: Distance matrix API response
    '''
    api_responses = {}
    base_url = "https://api.distancematrix.ai/maps/api/distancematrix/json"
    # DB Get all
    stops = BUS_LOCATIONS_PARSED["locationStops"]
    bus_objects = get_all_buses(db=db)
    for bus_id, bus_coordinates in bus_objects.items():
        api_responses[bus_id] = []
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
                    api_responses[bus_id].append(data)
                else:
                    raise HTTPException(status_code=response.status_code, detail="No response from Distance Matrix Server")

    print(api_responses)


    return {"data" : api_responses}


@router.post("/postLocation")
async def post_location(
        lat: float,
        longitude: float,
        time: str,
        id: str,
        db: Session = Depends(get_db)
    ):
    '''
    GPS Logger Listener
    :param locationObj:
    :return: BOOL
    '''
    bus = add_or_update_bus(id, lat, longitude, time, db=db)
    return {"200", "Success"}