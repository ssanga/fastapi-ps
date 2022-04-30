import uvicorn
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel

from db import engine, get_session
from routers import cars, web

app = FastAPI(title="Car Sharing")
app.include_router(web.router)
app.include_router(cars.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
