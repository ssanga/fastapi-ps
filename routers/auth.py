from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select
from starlette import status

from db import get_session
from schemas import UserOutput, User

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security),
                    session: Session = Depends(get_session)) -> UserOutput:
    query = select(User).where(User.username == credentials.username)
    user = session.exec(query).first()
    if user and user.verify_password(credentials.password):
        return UserOutput.from_orm(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
        )


# def get_current_user(token: str = Depends(oauth2_scheme),
#                  session: Session = Depends(get_session)) -> UserOutput:
#     query = select(User).where(User.username == token)
#     user = session.exec(query).first()
#     if user:
#         return UserOutput.from_orm(user)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Username or password incorrect",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# @router.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(),
#                 session: Session = Depends(get_session)):
#     query = select(User).where(User.username == form_data.username)
#     user = session.exec(query).first()
#     if user and user.verify_password(form_data.password):
#         return {"access_token": user.username, "token_type": "bearer"}
#     else:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")