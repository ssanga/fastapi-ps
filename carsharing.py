from imp import reload
from typing import List, Optional
from fastapi import FastAPI, HTTPException
import uvicorn

from schemas import CarInput, CarOutput, load_db, save_db

app = FastAPI()

db = load_db()


@app.get("/api/cars")
def get_cars(size: Optional[str] = None, doors:Optional[int] = None) -> List:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    
    return result

@app.get("/api/cars/{id}")
def car_by_id(id : int) -> dict:
    if result := [car for car in db if car.id == id]:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.post("/api/cars", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, fuel=car.fuel, doors=car.doors, transmission=car.transmission, id=len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car

@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

@app.put("/api/cars/{id}", response_model=CarOutput)
def change_car(id: int, new_data: CarInput) -> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.size = new_data.size
        car.fuel = new_data.fuel
        car.doors = new_data.doors
        car.transmission = new_data.transmission
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

if __name__ == '__main__':
    uvicorn.run("carsharing:app", reload = True)