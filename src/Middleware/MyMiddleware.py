# built-in
import jwt
from fastapi import Request, Depends, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Annotated

# custom
from src.Security.Security import Security
from src.Models.UserModel import UserModel


class MyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        url = str(request.url)

        # if "docs" in str(request.url):
        #     response = await call_next(request)
        
        if "login" in str(request.url):
            response = await call_next(request)
        else:
            if "Authorization" in request.headers:
                authorization = request.headers.get("Authorization")
                if not authorization:
                    raise HTTPException(status_code=401, detail="Unauthorized")
                token = authorization.split("Bearer ")[1]
                user = Security.get_current_user(token=token)

                if "admin" in url and user.category != "admin":
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not an admin")

                if user:
                    request.state.user_id = user.id
                    response = await call_next(request)
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization failed")
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization is not present in headers")
    
        return response