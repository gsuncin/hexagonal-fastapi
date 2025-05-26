from fastapi.security import OAuth2PasswordBearer
from src.domain.interfaces.user_interface import UserInterface
from src.adapters.driven.database.user_repository import User
from src.domain.schema.auth_schema import TokenData, AuthEntity
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from passlib.context import CryptContext
from src.core import settings
from typing import Annotated
from jose import jwt
import pytz
from src.adapters.driven.database.base import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JWTAuth:
    pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    @classmethod
    def create_access_token(cls, key: str):
        """
        @key: {"key": "$user.key"}
        returns Bearer Token for auth and expire
        """
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(tz=pytz.timezone(settings.TIMEZONE)) + expires_delta
        to_encode = {"sub": key, "exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt, expire.astimezone(pytz.timezone(settings.TIMEZONE))

    @classmethod
    def verify_access_token(cls, token: Annotated[str, Depends(oauth2_scheme)]):
        """
        @data: {"document_id": "$user.document_id}
        @expires_delta: datetime.timedelta object
        returns Bearer Token for auth
        """
        try:
            db = SessionLocal()
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if not (key := payload.get("sub")):
                raise cls.credentials_exception
            user = User.filter(db, User.name == key).first()
            TokenData(key=key)
            return user
        except Exception as exc:
            print(exc)
            raise cls.credentials_exception

    @classmethod
    def error_exception(cls, detail: str):
        detail = detail
        cls.credentials_exception.detail = detail
        raise NameError(detail)


def login(form_data: AuthEntity, db):
    user_data = User.filter(db, User.email == form_data.username).first()
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect document_id or password")
    hashed_password = JWTAuth.pwd_crypt.verify(form_data.password, user_data.password)
    if not hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect document_id or password")
    key = user_data.email
    token, expire = JWTAuth.create_access_token(key)
    return {"access_token": token, "token_type": "bearer", "expire": expire}


def register_user(user_data, db):
    user_created = UserInterface.icreate(user_data, db, JWTAuth)
    return {"data": user_created}


token_jwt = Annotated[str, Depends(JWTAuth.verify_access_token)]
