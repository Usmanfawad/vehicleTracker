from fastapi import Query
from pydantic import BaseModel


class Location(BaseModel):
    lat: float = Query(..., description="Latitude of the location", example="47.8807676")
    longitude: float = Query(..., description="Longitude of the location", example="10.0403246")
    time: str = Query(..., description="The time the location was posted in ISO 8601 format", example="2024-03-25T11:48:37.136Z")
    bus_id: str = Query(..., description="A unique identifier for the bus. Basically the GPS logger bus ID", example="7143c08dd569876e")

    class Config:
        from_attributes = True