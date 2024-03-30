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
from app.routers.helpers import parse_distance_matrix_result


from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body, Form, FastAPI, Query


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
        print(BUS_LOCATIONS_PARSED)
        print("...Application startup complete...")

    except Exception as e:
        print(e)



@router.get("/bus_stops")
async def main():
    '''
    Test route
    :return: Coordinates list
    '''
    if BUS_LOCATIONS_PARSED is None:
        return {"error": "Application is not fully initialized yet."}
    return {"200": "Success", "data": BUS_LOCATIONS_PARSED}



@router.get("/distance/all", status_code=status.HTTP_200_OK)
async def get_distance_all(db: Session = Depends(get_db)):
    '''
    Returns distances of all busses from all the stops
    :return: Distance matrix API response
    '''
    api_responses_lst = []
    BASE_URL = "https://api.distancematrix.ai/maps/api/distancematrix/json"
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
                    response = await client.get(BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    parsed_result = parse_distance_matrix_result(data)
                    api_responses["distances"].append(parsed_result)
                else:
                    raise HTTPException(status_code=response.status_code, detail="No response from Distance Matrix Server")
        api_responses_lst.append(api_responses)

        sorted_data = sorted(api_responses_lst[0]["distances"], key=lambda x: x["in_m"])

    return {"data" : sorted_data}


@router.post("/bus_stop")
async def bus_stop(
        lat: float = Query(..., description="Latitude of the location", example="47.8807676"),
        longitude: float = Query(..., description="Longitude of the location", example="10.0403246"),
        time: str = Query(..., description="The time the location was posted in ISO 8601 format", example="2024-03-25T11:48:37.136Z"),
        id: str = Query(..., description="A unique identifier for the bus. Basically the GPS logger bus ID", example="7143c08dd569876e"),
        db: Session = Depends(get_db)
    ):
    print(lat)
    """
    GPS Logger Listener. Adds or updates location in DB.

    - **lat**: Latitude of the bus stop.
    - **longitude**: Longitude of the bus stop.
    - **time**: The time the bus stop was recorded. Expected format: ISO 8601. example="2024-03-25T11:48:37.136Z"
    - **bus_id**: A unique identifier for the bus.
    """
    bus = add_or_update_bus(id, lat, longitude, time, db=db)
    return {"200", "Success"}