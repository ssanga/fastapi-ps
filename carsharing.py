import uvicorn
from fastapi import Depends, FastAPI, Request
from sqlmodel import SQLModel

from db import engine, get_session
from routers import cars, web
from routers.cars import BadTripException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="Car Sharing")
app.include_router(web.router)
app.include_router(cars.router)

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.exception_handler(BadTripException)
async def unicorn_exception_handler(request: Request, exc: BadTripException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content = {"message": "Bad Trip"}
    )
    

@app.middleware("http")
async def add_cars_cookie(request: Request, call_next):
    response = await call_next(request)
    response.set_cookie("cars_cookie", "this_is_a_cookie")
    return response

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
