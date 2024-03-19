from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.bus import Bus



def add_or_update_bus(id: int, lat: float, lon: float, time: str, db: Session):
    try:
        # Attempt to find an existing bus by ID
        bus = db.query(Bus).filter(Bus.bus_id == id).first()

        if bus:
            # If the bus exists, update its lat, lon, and time
            bus.lat = lat
            bus.lon = lon
            bus.time = time
            print(f"Updated Bus {id} with new values.")
        else:
            # If the bus does not exist, create a new one
            bus = Bus(bus_id=id, lat=lat, lon=lon, time=time)
            db.add(bus)
            print(f"Added new Bus with ID {id}.")

        db.commit()
        return bus
    except IntegrityError as e:
        db.rollback()
        print(f"Failed to add or update the bus due to an integrity error: {e}")
        return None


def get_all_buses(db: Session):
    buses = db.query(Bus).all()  # Query all busses from the database
    bus_dict = {}
    for bus in buses:
        bus_dict[str(bus.bus_id)] = [bus.lat, bus.lon]
    return bus_dict