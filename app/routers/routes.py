import httpx
import os
import json
import asyncio

from sqlalchemy.orm import Session

from app.services.utils.lat_long_parser import extract_coordinates
from app.routers.constants import *
from app.db.session import get_db
from app.services.controllers.bus import add_or_update_bus, get_all_buses, delete_all_buses
from app.routers.helpers import parse_distance_matrices
from app.schemas.schema import ImageData

from app.models.bus import Bus


from typing import Any

from fastapi import APIRouter, HTTPException, Depends, status, Query



router = APIRouter(
    prefix="/v1",
    tags=["main"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

BUS_LOCATIONS_PARSED = None
LAST_STOPS = {}


@router.on_event("startup")
async def lifespan():
    global BUS_LOCATIONS_PARSED
    try:
        cwd = os.getcwd()
        json_file_path = os.path.join(cwd, 'app', 'routers', 'constants.json')
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
    BASE_URL = "https://api.distancematrix.ai/maps/api/distancematrix/json"
    # Assume BUS_LOCATIONS_PARSED and get_all_buses are defined elsewhere
    stops = BUS_LOCATIONS_PARSED["locationStops"]
    bus_objects = get_all_buses(db=db)

    async def fetch_distances(bus_id, bus_coordinates, stops):
        distances = []
        # Example optimization: combining stops into a single 'destinations' parameter if API supports it
        # Adjust based on API limitations
        destinations = "|".join(",".join(map(str, stop.values())) for stop in stops)
        destinations = destinations.replace("[", "").replace("]", "")

        params = {
            "origins": ",".join(map(str, bus_coordinates)),
            "destinations": destinations,
            "key": API_KEY
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)

        if response.json()["status"] != "REQUEST_DENIED":
            data = response.json()
            distances.append(parse_distance_matrices(data))
        else:
            raise HTTPException(status_code=500, detail=response.json())

        try:
            # Read the JSON file and return its content
            with open("images.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")


        counter = 0
        for each_obj in distances[0]:
            each_obj["destination"]["img_url"] = list(data["images"].values())[counter]
            each_obj["in_s"] += 60
            counter += 1


        bus = db.query(Bus).filter(Bus.bus_id == bus_id).first()
        print(bus_id)
        for i in range(len(distances[0])):
            dist = distances[0][i]
            if dist["in_m"] <= 200:
                bus.last_stop_index = i
                db.commit()
                print("SHOULD UPDATE NOW")
        last_bus_stop_index = bus.last_stop_index

        return {"bus_id": bus_id, "distances": distances[0], "last_bus_stop_index": last_bus_stop_index}

    tasks = [fetch_distances(bus_id, bus_coords, stops) for bus_id, bus_coords in bus_objects.items()]
    api_responses_lst = await asyncio.gather(*tasks)
    return {"data": api_responses_lst}


@router.post("/bus_stop", status_code=status.HTTP_201_CREATED)
async def bus_stop(
        lat: float = Query(..., description="Latitude of the location", example="47.8807676"),
        longitude: float = Query(..., description="Longitude of the location", example="10.0403246"),
        time: str = Query(..., description="The time the location was posted in ISO 8601 format", example="2024-03-25T11:48:37.136Z"),
        id: str = Query(..., description="A unique identifier for the bus. Basically the GPS logger bus ID", example="7143c08dd569876e"),
        db: Session = Depends(get_db)

    ):
    '''
    GPS Logger Listener. Adds or updates location in DB.

    - **lat**: Latitude of the bus stop.
    - **longitude**: Longitude of the bus stop.
    - **time**: The time the bus stop was recorded. Expected format: ISO 8601. example="2024-03-25T11:48:37.136Z"
    - **bus_id**: A unique identifier for the bus.
    '''

    bus = add_or_update_bus(id, lat, longitude, time, db=db)
    if bus.id:
        return {"Bus obj": bus}

    return {"Error" : "Unable to add or update bus "}


@router.delete("/bus/all")
def delete_bus_all(db: Session = Depends(get_db)):
    '''
    Endpoint to delete all bus objects from the Database
    :return:
    '''
    delete_busses = delete_all_buses(db=db)
    if delete_busses:
        return {"200": "Success"}

def custom_encoder(obj):
    """Custom JSON encoder function for Pydantic models."""
    if isinstance(obj, HttpUrl):
        print(obj)
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

@router.post("/upload-images/")
async def upload_images(image_data: ImageData):
    data_dict = image_data.dict()
    with open("images.json", "w") as file:
        json.dump(data_dict, file, default=custom_encoder, indent=4)
    return {"message": "Data saved successfully"}