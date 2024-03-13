from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

class Location(BaseModel):
    lat: float
    longitude: float
    time: str
    id: str
    # ?lat=%LAT&longitude=%LON&time=%TIME&id=%AID