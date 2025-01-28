# built-in
import jwt
from fastapi import status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone

# custom
from src.Security.HashGenerator import HashGenerator
from src.Persistance.database import get_db_session_instance
from src.Models.UserModel import UserModel

class TokenData(BaseModel):
    username: str | None = None

class Security:
    SECRET_KEY = "3e3bee7b9447a04fce9fe6312f3e9743dbfc49b67dddd49bbb3badb40180cb30"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    def __init__(self):
        pass

    @staticmethod
    def is_valid_user_and_password(username: str, password: str, db_session) -> bool:
        user = Security.get_user(username, db_session)
        if user and Security.verify_password(password, user.password):
            print(f"Verified user: {username}")
            return True
        return False

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return HashGenerator.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return HashGenerator.generate(password)
    
    @staticmethod
    def get_user(username: str, db_session: Session):
        user = db_session.query(UserModel).filter(UserModel.name == username).first()
        return user
    
    @staticmethod
    def create_access_token(data: dict, db_session: Session):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES)

        if not Security.is_valid_user_and_password(data["username"], data["password"], db_session):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No such user")

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Security.SECRET_KEY, algorithm=Security.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(token):
        db_session = get_db_session_instance()
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, Security.SECRET_KEY, algorithms=[Security.ALGORITHM])
            username: str = payload.get("username")

            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except jwt.ExpiredSignatureError:
            credentials_exception["detail"] = "Token expired"
            raise credentials_exception
        except jwt.InvalidTokenError:
            raise credentials_exception
        
        user = Security.get_user(token_data.username, db_session)
        if user is None:
            raise credentials_exception
        return user


