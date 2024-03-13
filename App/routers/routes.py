import httpx


from App.schemas.schema import Location
from App.services.utils.lat_long_parser import extract_coordinates


from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body, Form
from typing import Optional


FAKE_DB = {
    "5908kjhg": [47.609795, 7.659121]
}

BUS_STOPS = [
    "https://www.google.com/maps/place/47%C2%B036'35.0%22N+7%C2%B039'32.4%22E/@47.6097222,7.659,19z/data=!3m1!4b1!4m4!3m3!8m2!3d47.6097222!4d7.659?entry=ttu",
    "https://www.google.com/maps/place/47%C2%B036'50.6%22N+7%C2%B039'53.0%22E/@47.6140495,7.6636721,18z/data=!3m1!4b1!4m4!3m3!8m2!3d47.614048!4d7.664716?entry=tts",
    "https://www.google.com/maps/place/47%C2%B037'05.6%22N+7%C2%B039'35.9%22E/@47.6182219,7.6593173,19z/data=!3m1!4b1!4m4!3m3!8m2!3d47.618221!4d7.659961?entry=tts",
    "https://www.google.com/maps/place/47%C2%B037'56.0%22N+7%C2%B040'49.5%22E/@47.6322209,7.6792053,19z/data=!3m1!4b1!4m4!3m3!8m2!3d47.63222!4d7.680423?entry=tts",
    "https://www.google.com/maps/place/47%C2%B038'06.3%22N+7%C2%B040'47.2%22E/@47.6350889,7.6785513,19z/data=!3m1!4b1!4m4!3m3!8m2!3d47.635088!4d7.679769?entry=tts"
]

API_KEY = "19R52Ym2JIhq6P8YUd5E68gozFzSbT7VsSOiAtfL3BReQDZOUeJEvcgmpox1Jq6O"


bus_locations_parsed = {
    "locationStops": [
        { "stopOne": [
          47.6097222,
          7.659
        ]},
        { "stopTwo": [
          47.6140495,
          7.6636721
        ]},
        { "stopThree": [
          47.6182219,
          7.6593173
        ]},
        { "stopFour": [
          47.6322209,
          7.6792053
        ]},
        { "stopFive": [
          47.6350889,
          7.6785513
        ]}
  ]
}


router = APIRouter(
    prefix="/v1",
    tags=["main"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def main():
    coordinates_list = [extract_coordinates(url) for url in BUS_STOPS]
    return {"200": "Success", "data": coordinates_list}


@router.get("/getDistance/all")
async def get_distance_all():
    '''
    Returns distances of all busses from all the stops
    :return:
    '''
    distance_matrix_endpoint = f'https://api.distancematrix.ai/maps/api/distancematrix/json?origins=51.4822656,-0.1933769&destinations=51.4994794,-0.1269979&key=19R52Ym2JIhq6P8YUd5E68gozFzSbT7VsSOiAtfL3BReQDZOUeJEvcgmpox1Jq6O'

    # DB Get all
    stops = bus_locations_parsed["locationStops"]
    # Iterate
    for bus_id, bus_coordinates in FAKE_DB.items():
        print(bus_id, bus_coordinates)
        for each_stop in stops:
            for stop, coordinates in each_stop.items():
                print(stop, coordinates)
    return {"200", "Success"}


@router.get("/getDistance")
async def get_distance(bus_id: int):
    '''
    Returns distance of a particular bus from all the stops
    :return:
    '''
    # DB Get bus
    # Iterate
    return {"200", "Success"}


@router.post("/postLocation")
async def post_location(location_obj: Location):
    '''
    GPS Logger Listener
    :param locationObj:
    :return:
    '''
    print(location_obj)
    return {"200", "Success"}