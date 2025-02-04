# built-in
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# custom
from src.Models import UserModel, BookModel, Borrowings
from src.Persistance.database import Base, db_engine
from src.Routers.LibrarianRouter import librarian_router
from src.Routers.UserRouter import user_router
from src.Middleware.MyMiddleware import MyMiddleware
from src.Security.Security import Security
from src.Schema.TokenSchema import TokenSchema
from src.Persistance.database import get_db_session, get_db_session_instance
from src.Security.HashGenerator import HashGenerator


class LibrarySystem(FastAPI):
    def __init__(self):
        super().__init__()
        self.add_middleware(MyMiddleware)
        self.initialize_endpoints()
        Base.metadata.create_all(db_engine)

    def initialize_endpoints(self):
        self.add_api_route("/health",
                           self.get_health,
                           status_code=status.HTTP_202_ACCEPTED)
        self.add_api_route("/login",
                           self.login_user,
                           methods=["POST"],
                           status_code=status.HTTP_202_ACCEPTED)
        self.include_router(librarian_router)
        self.include_router(user_router)
    
    def login_user(self, data: Annotated[OAuth2PasswordRequestForm, Depends()], db_session: Session = Depends(get_db_session)) -> TokenSchema:
        access_token, user = Security.create_access_token({"username": data.username, "password": data.password}, db_session)
        if access_token is None:
            print(f"HERE")
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="No Such user")

        user_dict = {"name": user.name,
                     "category": user.category}
        
        return TokenSchema(access_token=access_token, token_type="bearer", user=user_dict)

    def get_health(self):
        return JSONResponse({
            "message": "We are Innn"
        })

        