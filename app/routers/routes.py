import httpx
from typing import Optional
import os
import json

from sqlalchemy.orm import Session


from app.schemas.schema import Location
from app.services.utils.lat_long_parser import extract_coordinates
from app.routers.constants import *
from app.db.session import get_db
from app.services.controllers.bus import add_or_update_bus, get_all_buses
from app.routers.helpers.helpers import parse_distance_matrix_result


from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body, Form, FastAPI


from contextlib import asynccontextmanager




router = APIRouter(
    prefix="/v1",
    tags=["main"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

BUS_LOCATIONS_PARSED = None


@router.on_event("startup")
async def lifespan():
    global BUS_LOCATIONS_PARSED
    try:
        cwd = os.getcwd()
        json_file_path = os.path.join(cwd, 'app', 'routers', 'constants.json')
        print(json_file_path)
        with open(json_file_path, 'r') as file:
            constants = json.load(file)

        location_stops = []
        for key, value in constants.items():
            coordinates = extract_coordinates(value)
            if coordinates:
                location_stops.append({key: coordinates})

        # Construct the desired structure
        BUS_LOCATIONS_PARSED = {"locationStops": location_stops}

        print("...Application startup complete...")

    except Exception as e:
        print(e)



@router.get("/main")
async def main():
    '''
    Test route
    :return: Coordinates list
    '''
    if BUS_LOCATIONS_PARSED is None:
        return {"error": "Application is not fully initialized yet."}
    return {"200": "Success", "data": BUS_LOCATIONS_PARSED}



@router.get("/getDistance/all", status_code=status.HTTP_200_OK)
async def get_distance_all(db: Session = Depends(get_db)):
    '''
    Returns distances of all busses from all the stops
    :return: Distance matrix API response
    '''
    api_responses_lst = []
    base_url = "https://api.distancematrix.ai/maps/api/distancematrix/json"
    # DB Get all
    stops = BUS_LOCATIONS_PARSED["locationStops"]
    bus_objects = get_all_buses(db=db)
    for bus_id, bus_coordinates in bus_objects.items():
        api_responses = {}
        api_responses["bus_id"] = bus_id
        api_responses["distances"] = []
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
                    parsed_result = parse_distance_matrix_result(data)
                    api_responses["distances"].append(parsed_result)
                else:
                    raise HTTPException(status_code=response.status_code, detail="No response from Distance Matrix Server")
        api_responses_lst.append(api_responses)

    return {"data" : api_responses_lst}


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