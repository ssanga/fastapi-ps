import json
from pydantic import BaseModel


class CarInput(BaseModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

class CarOutput(CarInput):
    id: int

def load_db() -> list[CarOutput]:
    """Load a list of Car objects from a JSON file"""
    with open("cars.json", "r") as f:
        return [CarOutput.parse_obj(car) for car in json.load(f)]

def save_db(cars: list[CarInput]) -> None:
    """Save a list of Car objects to a JSON file"""
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)