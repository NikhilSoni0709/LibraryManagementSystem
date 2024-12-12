# built-in
import jwt
from fastapi import Request, Depends, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
# from fastapi.security import HTTPBearer
from typing import Annotated

# custom
from src.Security.Security import Security
from src.Models.UserModel import UserModel

# security = HTTPBearer(auto_error=False)

class MyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Do something before the request is handled
        print(request.url)
        if "login" not in str(request.url):
            authorization = request.headers.get("Authorization")
            if not authorization:
                raise HTTPException(status_code=401, detail="Unauthorized")
            token = authorization.split("Bearer ")[1]
            user = Security.get_current_user(token=token)
            if user:
                response = await call_next(request)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="something is wrong")
        else:
            response = await call_next(request)
        # Do something after the response is generated
        print(f"Check here")
        return response